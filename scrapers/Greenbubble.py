import re

from bs4 import BeautifulSoup
from web_scraping.product import Product, parse_str

# TODO: Put this in a config file
BASE_URL = "https://www.green-bubble.com/en/all-houseplants"
NUM_PAGES = 5


def get_urls() -> list[str]:
    return [BASE_URL + f"/page{str(i+1)}.html?limit=100" for i in range(NUM_PAGES)]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ul", class_="list-collection")

    products = []

    # Loop through the products
    for product in products_div.find_all("li", attrs={"data-url": True}):  # type: ignore # None possible
        # Get the product information
        name = parse_str(product.find("h3").text)
        description = parse_str(product.find("div", class_="overview-specs").text)
        price = product.find("p", class_="price")
        price_span = price.find("span", class_=False)
        price = price_span.text if price_span else price.text
        price = _parse_price(price)
        link = parse_str(product.find("a", href=True)["href"])

        # Add the product to the list
        products.append(Product(name, description, price, link))

    return products
