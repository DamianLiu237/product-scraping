import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://homedeco.nl/kamerplant"
NUM_PAGES = 69


def get_urls() -> list[str]:
    return [BASE_URL + f"/?page={i+1}" for i in range(NUM_PAGES)]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("div", class_="flex-products")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("div", class_="flex-item"):  # type: ignore # None possible:
        # Get the product information
        name = product.parse_str(product_element.find("div", class_="prod-name").text)
        description = product.parse_str(
            product_element.find("div", class_="prod-brand").text
        )
        link = product.parse_str(
            product_element.find("div", class_="prod-name").a["href"]
        )

        price = _parse_price(
            product_element.find("div", class_="prod-price").a.contents[0].text
        )

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
