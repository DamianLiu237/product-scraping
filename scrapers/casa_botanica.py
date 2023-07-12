import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://casa-botanica.com/nl/producten/?limit=50"
NUM_PAGES = 5


def get_urls() -> list[str]:
    return [BASE_URL + f"&page={str(i + 1)}" for i in range(NUM_PAGES)]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ul", class_="c-producten__list")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li"):  # type: ignore # None possible:
        name = product_element.find("h3", class_="c-product-thumb__title")
        if name:
            name = product.parse_str(name.text)

        description = product_element.find("ul", class_="eigenschappen")
        if description:
            description = product.parse_str(description.text)

        price = product_element.find(
            "div", class_="o-price o-price--small c-product-thumb__price"
        )
        if price:
            price = _parse_price(price.text)

        link = product_element.find("a", class_="c-product-thumb", href=True)
        if link:
            link = product.parse_str(link["href"])

        if all(not x for x in [name, description, price, link]):
            continue

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
