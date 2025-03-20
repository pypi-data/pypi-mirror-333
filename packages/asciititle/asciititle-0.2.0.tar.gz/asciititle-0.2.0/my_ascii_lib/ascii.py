# my_ascii_lib/ascii.py
from .font_loader import FONTS

def ascii_art(text, font="blurvision", sep=" "):
    """
    Generate ASCII art for the given text using the specified font.
    
    :param text: The string to convert into ASCII art.
    :param font: Either a font name (string) to look up in FONTS, or a font dictionary.
    :param sep: The string inserted between characters (default is one space).
    :return: A string containing the rendered ASCII art.
    """
    # Look up the font if a string is provided.
    if isinstance(font, str):
        font_data = FONTS.get(font.lower())
        if not font_data:
            raise ValueError(f"Font '{font}' not found. Available fonts: {list(FONTS.keys())}")
    else:
        font_data = font

    # Assume all characters have the same number of lines.
    height = len(next(iter(font_data.values())))
    art_lines = [""] * height

    for char in text.upper():
        # Retrieve the ASCII art for the character; if missing, use a blank placeholder.
        char_art = font_data.get(char)
        if not char_art:
            any_art = next(iter(font_data.values()))
            width = len(any_art[0])
            char_art = [" " * width] * height
        # Append each line of the character's art plus the separator.
        for i in range(height):
            art_lines[i] += char_art[i] + sep

    return "\n".join(art_lines)
