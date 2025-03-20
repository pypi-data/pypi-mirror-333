import unicodedata
import re
import string
import sys
from sanitext.homoglyph_map import get_homoglyph_replacement
from sanitext.emoji_set import EMOJI_SET


def get_allowed_characters(allow_emoji=False, allow_chars=None, allow_file=None):
    """
    Build and return the set of allowed characters based on:
      - default ASCII printable
      - user-specified flag to allow single code point emojis
      - user-specified chars
      - user-specified file (pathlib.Path object)
    """
    allowed = set(string.printable)

    if allow_emoji:
        allowed.update(EMOJI_SET)

    # If user provides extra chars via CLI:
    if allow_chars:
        allowed.update(set(allow_chars))

    # If user provides a file of allowed chars:
    if allow_file:
        text_from_file = allow_file.read_text(encoding="utf-8", errors="replace")
        allowed.update(text_from_file)

    return allowed


def sanitize_text(text, allowed_characters=get_allowed_characters(), interactive=False):
    """
    Remove or replace characters not in the allowed set. Optionally prompt the user interactively.
    Returns the sanitized text.
    """
    # Identify disallowed characters
    disallowed_chars = sorted(set(ch for ch in text if ch not in allowed_characters))
    if not disallowed_chars:
        # If nothing disallowed, just return original text
        return text

    # If interactive is enabled, ask the user for each unique disallowed char
    char_decisions = {}
    if interactive:
        for ch in disallowed_chars:
            # Decision for this character already been taken
            if ch in char_decisions:
                continue
            # Provide some info about the character
            char_info = f"'{ch}' (U+{ord(ch):04X}, {unicodedata.name(ch, 'Unknown')})"
            while True:
                decision = (
                    input(
                        f"Character {char_info} is not allowed. Keep [y], Remove [n], or Replace [r]? "
                    )
                    .strip()
                    .lower()
                )
                if decision in ("y", "n", "r"):
                    if decision == "y":
                        # Keep => add to allowed set for this run
                        char_decisions[ch] = ch
                    elif decision == "n":
                        # Remove => map to empty string
                        char_decisions[ch] = ""
                    else:
                        # Replace => ask user for replacement
                        replacement = input("Enter replacement character(s): ")
                        char_decisions[ch] = replacement
                    break
                else:
                    print("Invalid input. Please enter 'y', 'n', or 'r'.")
    else:
        for ch in disallowed_chars:
            closest = closest_ascii(ch, allowed_characters)
            char_decisions[ch] = (
                closest if set(closest).issubset(allowed_characters) else ""
            )

    # Build the sanitized text
    sanitized_chars = []
    for ch in text:
        if ch in disallowed_chars:
            sanitized_chars.append(char_decisions[ch])
        else:
            sanitized_chars.append(ch)

    return "".join(sanitized_chars)


def closest_ascii(char, allowed_characters):
    """Returns the closest ASCII character for a given Unicode character."""
    # Try homoglyph replacement first
    mapped = get_homoglyph_replacement(char)
    if mapped in allowed_characters:
        return mapped  # Direct replacement

    # Try Unicode normalization (NFKC)
    normalized = unicodedata.normalize("NFKC", char)
    if all(c in allowed_characters for c in normalized):
        return normalized  # Safe replacement

    # Try Unicode decomposition
    # Examples:
    #   'é' (U+00E9) decomposes to 'e' + ◌́ (acute accent).
    #   Ⅵ (U+2165) decomposes to 'V' + 'I'
    #   ﬁ (U+FB01) decomposes to 'f' + 'i'
    decomposed = unicodedata.decomposition(char)
    if decomposed:
        # Remove non-hex parts (e.g., "<compat>")
        hex_parts = [
            part
            for part in decomposed.split()
            if all(c in "0123456789ABCDEF" for c in part)
        ]
        # Convert hex to ASCII characters
        ascii_chars = [chr(int(part, 16)) for part in hex_parts if int(part, 16) < 128]
        # Only keep allowed characters
        ascii_chars = [c for c in ascii_chars if c in allowed_characters]
        return "".join(ascii_chars) if ascii_chars else ""

    # If no good match, return ""
    return ""


def detect_suspicious_characters(text, allowed_characters=get_allowed_characters()):
    """
    Finds characters in the text that are not ASCII letters, digits, punctuation, or common whitespace.

    Args:
        text (str): The input text to check.
        allowed_characters (set): Set of allowed characters

    Returns:
        list of tuple: A list of tuples, each containing a suspicious character and its Unicode name.
    """
    return [
        (char, unicodedata.name(char, "Unknown"))
        for char in text
        if char not in allowed_characters
    ]
