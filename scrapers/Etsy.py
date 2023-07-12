import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.etsy.com/nl/c/home-and-living/outdoor-and-garden/plants/house-plants?locationQuery=2750405&ref=pagination"
NUM_PAGES = 17

PRODUCTS_DIV_CLASS = "wt-grid wt-grid--block wt-pl-xs-0 tab-reorder-container"
DESCRIPTION_CLASS = (
    "wt-text-caption wt-text-truncate wt-text-grey wt-mb-xs-1 min-height"
)


def get_urls() -> list[str]:
    urls = [BASE_URL + f"&page={str(i + 1)}" for i in range(NUM_PAGES)]
    return urls


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ol", class_=PRODUCTS_DIV_CLASS)

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li", recursive=False):  # type: ignore # None possible:
        name = product_element.find("h3")
        if name:
            name = product.parse_str(name.text)

        description_pattern = re.compile(r"wt-text-caption wt-text-truncate")
        description = product_element.find("div", class_=description_pattern)
        if description:
            description = description.text.split()[-1]
            description = product.parse_str(description)

        wo_discount = product_element.find("span", class_="wt-text-strikethrough")
        if wo_discount:
            price = wo_discount.find("span", class_="currency-value")
        else:
            price = product_element.find("span", class_="currency-value")
        if price:
            price = _parse_price(price.text)

        link = product_element.find("a", href=True)
        if link:
            link = product.parse_str(link["href"])

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
