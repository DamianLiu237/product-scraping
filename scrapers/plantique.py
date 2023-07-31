import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://plantique.shop/collections/alle-planten"
NUM_PAGES = 9


def get_urls() -> list[str]:
    return [BASE_URL + f"?page={str(i + 1)}" for i in range(NUM_PAGES)]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("div", class_="grid grid--uniform")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("div", class_="grid-product__content"):  # type: ignore # None possible:
        name = product_element.find(
            "div", class_="grid-product__title grid-product__title--heading"
        )
        if name:
            name = product.parse_str(name.text)

        description = product_element.find(
            "span", class_="grid-product__price--savings"
        )
        if description:
            description = product.parse_str(description.text)

        price = product_element.find("div", class_="grid-product__price")
        orig_price = price.find("span", class_="grid-product__price--original")

        if orig_price:
            price = _parse_price(orig_price.text)
        elif price:
            price = _parse_price(price.text)

        link = product_element.find("a", href=True)
        if link:
            link = product.parse_str("https://plantique.shop" + link["href"])

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
