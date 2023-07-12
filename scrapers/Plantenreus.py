import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://plantenreus.nl/kamerplanten/"
NUM_PAGES = 67

PRODUCTS_DIV_CLASS = "module woocommerce module-advanced-products tb_ks7q335 themify_builder_content-ks7q335"


def get_urls() -> list[str]:
    urls = [BASE_URL + f"page/{str(i + 1)}/" for i in range(NUM_PAGES)]
    urls.pop(0)
    return urls


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,.]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("div", class_=PRODUCTS_DIV_CLASS)

    products = []

    # Loop through the products
    for product_element in products_div.find_all("div", class_="tbp_advanced_archive_wrap"):  # type: ignore # None possible:
        name = product_element.find("h2", class_="tbp_title")
        if name:
            name = product.parse_str(name.text)

        description = product_element.find("div", class_="tb_text_wrap")
        if description:
            description = product.parse_str(description.text)

        price = product_element.find("p", class_="price")
        if price:
            price = _parse_price(price.text)

        link = product_element.find("a", href=True)["href"]
        if link:
            link = product.parse_str(link)

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
