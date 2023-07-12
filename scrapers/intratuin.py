import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.intratuin.nl/kamerplanten/groene-kamerplanten"
NUM_PAGES = 56


def get_urls() -> list[str]:
    return [BASE_URL + f"?p={str(i + 1)}" for i in range(NUM_PAGES)]


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ol", class_="products list items product-items")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li", recursive=False):  # type: ignore # None possible:
        name = product_element.find("a", class_="product-item-link")
        if name:
            name = product.parse_str(name.text)

        description = product_element.find("div", class_="rating-result")
        num_reviews = product_element.find("span", class_="reviews-action-link")
        if description:
            description = product.parse_str(
                f"{description.text} from {num_reviews.text} reviews"
            )

        price = product_element.find("span", class_="price")
        if price:
            price = product.parse_price(price.text)

        link = product_element.find("a", href=True)
        if link:
            link = product.parse_str(link["href"])

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
