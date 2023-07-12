import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.dealdonkey.com/huis-en-tuin/planten-en-bomen-voor-binnen"
NUM_PAGES = 5


def get_urls() -> list[str]:
    return [BASE_URL]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("div", class_="products product-grid")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li", class_="small-12 medium-4 large-3 columns"):  # type: ignore # None possible:
        name = product_element.find("span", class_="prodName")
        if name:
            name = product.parse_str(name.text)

        description = product_element.find("span", class_="discount")
        if description:
            description = product.parse_str(description.text)

        price = product_element.find("span", class_="price special-price")
        if price:
            price = _parse_price(price.text)

        link = product_element.find("a", href=True)["href"]
        if link:
            link = product.parse_str(link)

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
