import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.stekjesenzo.nl"
NUM_PAGES = 19


def get_urls() -> list[str]:
    return [
        BASE_URL + f"/page/{str(i + 1)}/?s&post_type=product" for i in range(NUM_PAGES)
    ]


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ul", class_="products columns-4")

    products = []

    products_iterator = products_div.find_all("li", class_=["product", "type-product"])  # type: ignore # None possible

    # Loop through the products
    for product_element in products_iterator:
        name = product_element.find("h2", class_="woocommerce-loop-product__title")
        if name:
            name = product.parse_str(name.text)

        price = product_element.find("span", class_="woocommerce-Price-amount amount")
        if price:
            price = product.parse_price(price.text)

        link = product_element.find("a", href=True)
        if link:
            link = product.parse_str(link["href"])

        # Add the product to the list
        products.append(product.Product(name, None, price, link))

    return products
