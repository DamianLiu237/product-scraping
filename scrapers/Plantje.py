import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.plantje.nl/kamerplanten"
NUM_PAGES = 19

PRODUCTS_DIV_CLASS = "products row row-small large-columns-4 medium-columns-3 small-columns-2 has-equal-box-heights equalize-box"
PRODUCTS_ITER_CLASS = "product-small box"

NAME_CLASS = "woocommerce-loop-product__title"
DESCRIPTION_CLASS = "woocommerce-loop-product__title"
PRICE_CLASS = "woocommerce-Price-amount amount"
LINK_CLASS = "woocommerce-LoopProduct-link woocommerce-loop-product__link"


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def get_urls() -> list[str]:
    urls = [BASE_URL + f"/page/{str(i + 1)}/?count=12" for i in range(NUM_PAGES)]
    urls.pop(0)
    return urls


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ul", class_="products")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li"):  # type: ignore # None possible
        name = product_element.find("strong", class_=NAME_CLASS)
        if name:
            name = product.parse_str(name.contents[0].text)

        description = product_element.find("strong", class_=DESCRIPTION_CLASS)
        if description:
            description = product.parse_str(description.text)

        price = product_element.find("span", class_=PRICE_CLASS)
        if price:
            price = _parse_price(price.text)

        link = product_element.find("a", href=True)["href"]
        if link:
            link = product.parse_str(link)

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
