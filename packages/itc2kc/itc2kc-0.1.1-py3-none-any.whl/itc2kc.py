#!/usr/bin/env python3
import argparse
import itertools
import sys
from collections import defaultdict
from pathlib import Path
from typing import TextIO, Literal

from lxml import etree

ColorKeys = Literal["red", "green", "blue"]
ColorMapping = dict[str, dict[ColorKeys, int]]


def color_value_xpath(color: ColorKeys) -> str:
    color_upper = color[0].upper() + color[1:]
    return f"key[text() = '{color_upper} Component']/following-sibling::real[1]/text()"


def color_value(dict_elem: etree._Element, color: ColorKeys) -> float:
    xpath = color_value_xpath(color)
    # xpath returns a list, select first element
    return float(dict_elem.xpath(xpath)[0])


def color_values(dict_elem: etree._Element) -> tuple[float, float, float]:
    red = color_value(dict_elem, "red")
    green = color_value(dict_elem, "green")
    blue = color_value(dict_elem, "blue")
    return (red, green, blue)


def parse_itermcolors(itermcolors_file: TextIO) -> ColorMapping:
    """Parse an .itermcolors file and extract color values using lxml."""
    tree = etree.parse(itermcolors_file)
    root = tree.getroot()

    # Initialize a dictionary to store the colors
    colors: ColorMapping = defaultdict(dict)

    # Find the main dict which contains all color definitions, xpath returns a list
    main_dict = root.xpath("dict")[0]
    if main_dict is None:
        raise ValueError("Invalid .itermcolors file format - missing main dict")

    # Process all children of the main dict in pairs (key, dict)
    # Use itertools to batch the iterator
    try:
        for key_elem, dict_elem in itertools.batched(main_dict, 2):
            color_name = key_elem.text

            red, green, blue = color_values(dict_elem)

            if red is not None and green is not None and blue is not None:
                colors[color_name] = {
                    "red": int(red * 255),
                    "green": int(green * 255),
                    "blue": int(blue * 255),
                }
            else:
                print(f"itermcolors file malformed, {color_name} missing red, green, blue value")
                sys.exit(1)
    except ValueError:
        print("itermcolors file malformed, <key>/<dict> pair missing")
        sys.exit(1)

    return colors


def color_to_kitty_format(color: dict[ColorKeys, int]) -> str:
    """Convert a color dict to kitty format (#rrggbb)."""
    return f"#{color['red']:02x}{color['green']:02x}{color['blue']:02x}"


def generate_kitty_conf_lines(
    color_mapping: dict[str, str], colors: ColorMapping, kitty_conf: list[str]
) -> None:
    for kitty_name, iterm_name in color_mapping.items():
        if iterm_name in colors:
            kitty_conf.append(f"{kitty_name} {color_to_kitty_format(colors[iterm_name])}")


def create_kitty_config(colors: ColorMapping, theme_name: str) -> str:
    """Create a kitty.conf theme file from the color dict."""
    # Mapping from iTerm2 color names to kitty color names
    color_mapping = {
        "color0": "Ansi 0 Color",  # black
        "color1": "Ansi 1 Color",  # red
        "color2": "Ansi 2 Color",  # green
        "color3": "Ansi 3 Color",  # yellow
        "color4": "Ansi 4 Color",  # blue
        "color5": "Ansi 5 Color",  # magenta
        "color6": "Ansi 6 Color",  # cyan
        "color7": "Ansi 7 Color",  # light gray
        "color8": "Ansi 8 Color",  # dark gray
        "color9": "Ansi 9 Color",  # bright red
        "color10": "Ansi 10 Color",  # bright green
        "color11": "Ansi 11 Color",  # bright yellow
        "color12": "Ansi 12 Color",  # bright blue
        "color13": "Ansi 13 Color",  # bright magenta
        "color14": "Ansi 14 Color",  # bright cyan
        "color15": "Ansi 15 Color",  # white
        "background": "Background Color",
        "foreground": "Foreground Color",
        "cursor": "Cursor Color",
        "cursor_text_color": "Cursor Text Color",
        "selection_background": "Selection Color",
        "selection_foreground": "Selected Text Color",
        # 'bold_color': 'Bold Color',      # Not found in kitty conf
        "url_color": "Link Color",
    }

    kitty_conf = [f"# Kitty theme converted from iTerm2 colors: {theme_name}"]

    # Write direct mapping values
    generate_kitty_conf_lines(color_mapping, colors, kitty_conf)

    # Indirect mapped values
    # These property names don't have direct matches to iTerm2's color scheme, so I'll guess with
    # appropriate ones
    indirect_mapping = {
        # window border and bell colors
        "active_border_color": "Ansi 7 Color",
        "inactive_border_color": "Ansi 8 Color",
        "bell_border_color": "Ansi 5 Color",
        "visual_bell_color": "Ansi 13 Color",
        # tab bar colors
        "active_tab_foreground": "Ansi 15 Color",
        "active_tab_background": "Ansi 7 Color",
        "inactive_tab_foreground": "Ansi 8 Color",
        "inactive_tab_background": "Ansi 0 Color",
        "tab_bar_background": "Ansi 0 Color",
        "tab_bar_margin_color": "Ansi 8 Color",
        # marked text colors
        "mark1_foreground": "Selected Text Color",
        "mark1_background": "Selection Color",
        "mark2_foreground": "Selected Text Color",
        "mark2_background": "Selection Color",
        "mark3_foreground": "Selected Text Color",
        "mark3_background": "Selection Color",
    }
    generate_kitty_conf_lines(indirect_mapping, colors, kitty_conf)

    return "\n".join(kitty_conf)


def main() -> None:
    parser = argparse.ArgumentParser(description="A converter for iTerm2 to kitty themes")
    parser.add_argument("input", help="Path to .itermcolors file")
    parser.add_argument(
        "--output",
        help="Path to save kitty configuration to. Defaults the input file name with a .conf"
        "extension",
    )
    args = parser.parse_args()

    input_file_path = Path(args.input)
    theme_name = input_file_path.stem
    output_file_path = Path(args.output if args.output is not None else f"{theme_name}.conf")

    if not input_file_path.exists():
        raise RuntimeError("Input .itermcolors file does not exist")

    if output_file_path.exists():
        confirmation = input(f"Do you want to overwrite {output_file_path}? y/n")
        if confirmation != "y":
            print(f"Received {confirmation}, aborting")
            sys.exit(1)

    try:
        with input_file_path.open() as input_file:
            colors = parse_itermcolors(input_file)
            kitty_conf = create_kitty_config(colors, theme_name)

            with open(output_file_path, "w") as f:
                f.write(kitty_conf)

            print(f"Successfully converted {input_file_path} to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
