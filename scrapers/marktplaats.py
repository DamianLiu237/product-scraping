import re

from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.marktplaats.nl/q/obliqua+peru/"
QUERIES = "/#offeredSince:Een%20week"
NUM_PAGES = 1


def get_urls() -> list[str]:
    return [
        "https://www.marktplaats.nl/l/huis-en-inrichting/kamerplanten/#q:anthurium+silver+blush"
    ]


def _parse_price(price: str) -> float:
    matches = re.findall(r"[0-9,]+", price)
    numbers_only = "".join(matches).replace(",", ".")

    return float(numbers_only)


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("ul", class_="hz-Listings hz-Listings--list-view")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("li"):  # type: ignore # None possible:
        name = product_element.find("h3", class_="hz-Listing-title")
        if name:
            name = product.parse_str(name.text)

        description = product_element.find(
            "p", class_="hz-Listing-description hz-text-paragraph"
        )
        listing_info = product_element.find(
            "div", class_="hz-Listing-group--price-date-feature"
        )
        seller_info = product_element.find("div", class_="hz-Listing--sellerInfo")
        ophalen = product_element.find("div", class_="hz-Listing-attributes")

        if description:
            description = product.parse_str(description.get_text(" ", strip=True))

        if listing_info:
            description += "LISTING_INFO: " + product.parse_str(
                listing_info.get_text(" ", strip=True)
            )

        if seller_info:
            description += "SELLER_INFO: " + product.parse_str(
                seller_info.get_text(" ", strip=True)
            )

        if ophalen:
            description += "OPHALEN: " + product.parse_str(
                ophalen.get_text(" ", strip=True)
            )

        price = product_element.find(
            "span", class_="hz-Listing-price hz-text-price-label"
        )

        if price and any(char.isdigit() for char in price.text):
            price = _parse_price(price.text)
        else:
            price = None

        link = product_element.find("a", href=True)
        if link:
            link = product.parse_str(f"https://www.marktplaats.nl{link['href']}")

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
