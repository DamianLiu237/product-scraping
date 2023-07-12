import re
from dataclasses import dataclass

# TODO: put this in a config file
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


@dataclass(frozen=True)
class Product:
    """Class for the products"""

    name: str | None
    description: str | None
    price: float | None
    link: str | None


def parse_str(string: str) -> str:
    """Parse the product to a string"""

    return string.strip()


def parse_price(price: str, seperator_is_comma: bool = False) -> float:
    """Parse the price to a float"""

    seperator = "." if seperator_is_comma else ""

    # Remove all characters except for numbers and commas
    matches = re.findall(r"[0-9,.]+", price)
    numbers_only = "".join(matches).replace(",", seperator)

    return float(numbers_only)
