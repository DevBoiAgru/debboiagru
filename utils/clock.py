# Utility functions needed for the terminal clock

import json

with open("assets/ascii_numbers.json", "rb") as ascii_numbers:
    content = ascii_numbers.read().decode("utf-8")
    numbers = json.loads(content)


def ascii_num(num: str, sep: str = " "):
    """
    Converts a string of numbers into their ASCII art representation.
    Supported symbols: 0-9 / ;

    Args:
        num (str): A string of numerical characters to be converted.
        sep (str, optional): A separator to use between the ASCII art representations of the numbers. Defaults to a space.

    Returns:
        str: A string containing the ASCII art representation of the input numbers.
    """
    result = ""
    # Each ascii art number is 7 lines high
    for i in range(8):
        for char in num:
            result += numbers[char][i] + sep
        result += "\n"
    return result
