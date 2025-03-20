# my_ascii_lib/font_loader.py
import os
import json

def load_fonts(directory):
    fonts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            font_name = os.path.splitext(filename)[0].lower()  # e.g., 'blurvision'
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Process each character's art without stripping whitespace.
                for char, art in data.items():
                    if isinstance(art, str):
                        # Split into lines, preserving whitespace.
                        lines = art.splitlines()
                    elif isinstance(art, list):
                        # Keep the list as-is.
                        lines = art
                    else:
                        lines = []
                    data[char] = lines
                fonts[font_name] = data
    return fonts

FONTS = load_fonts(os.path.join(os.path.dirname(__file__), "fonts"))
