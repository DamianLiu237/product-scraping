from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://www.growjungle.com/"
NUM_PAGES = 13

PRODUCTS_DIV_CLASS = "products row row-small large-columns-4 medium-columns-3 small-columns-2 has-equal-box-heights equalize-box"
PRODUCTS_ITER_CLASS = "product-small box"
NAME_CLASS = "woocommerce-LoopProduct-link woocommerce-loop-product__link"
DESCRIPTION_CLASS = "category uppercase is-smaller no-text-overflow product-cat op-7"
PRICE_CLASS = "woocommerce-Price-amount amount"


def get_urls() -> list[str]:
    return [
        BASE_URL + f"page/{str(i + 1)}/?product_cat&s&post_type=product"
        for i in range(NUM_PAGES)
    ]


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("div", class_=PRODUCTS_DIV_CLASS)

    products = []

    # Loop through the products
    for product_element in products_div.find_all("div", class_=PRODUCTS_ITER_CLASS):  # type: ignore # None possible
        # Get the product information
        name = product.parse_str(product_element.find("a", class_=NAME_CLASS).text)
        description = product.parse_str(
            product_element.find("p", class_=DESCRIPTION_CLASS).text
        )
        price = product.parse_price(
            product_element.find("span", class_=PRICE_CLASS).text
        )
        link = product.parse_str(product_element.find("a", href=True)["href"])

        # Add the product to the list
        products.append(product.Product(name, description, price, link))

    return products
