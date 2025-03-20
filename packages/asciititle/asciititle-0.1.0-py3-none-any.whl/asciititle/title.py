from custom_fonts import CUSTOM_FONTS

def generate_title(text, font='slant'):
    """
    Generate an ASCII art title using a custom font.

    :param text: The text to convert.
    :param font: The font key to use from CUSTOM_FONTS.
    :return: A string with the ASCII art.
    """
    if font not in CUSTOM_FONTS:
        raise ValueError(f"Font '{font}' is not defined.")
    
    char_map = CUSTOM_FONTS[font]
    
    # Assume each character's ASCII art has the same number of lines.
    sample_char = next(iter(char_map.values()))
    height = len(sample_char)
    output_lines = [""] * height
    
    # Process each character in the input text
    for ch in text.upper():
        # Use a space if the character is not defined in the font
        if ch not in char_map:
            ch = ' '  # fallback to space or handle differently
        
        # Append each corresponding line for the character.
        for i in range(height):
            output_lines[i] += char_map[ch][i] + " "  # add a space between letters
    
    return "\n".join(output_lines)

# Example usage:
if __name__ == "__main__":
    title = generate_title("AB BA", font='slant')
    print(title)
