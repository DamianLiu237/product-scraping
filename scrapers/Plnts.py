from bs4 import BeautifulSoup
from web_scraping import product

# TODO: Put this in a config file
BASE_URL = "https://plnts.com/nl/shop/all-plnts"
NUM_PAGES = 24

PRODUCTS_DIV_CLASS = "products row row-small large-columns-4 medium-columns-3 small-columns-2 has-equal-box-heights equalize-box"
PRODUCTS_ITER_CLASS = "product-small box"

NAME_CLASS_PARENT = "text-sm italic leading-none lg:text-base 3xl:text-base"
NAME_CLASS = "truncate m-0 font-sans text-sm font-bold leading-tight 3xl:text-base"

PRICE_WO_DISCOUNT_CLASS = "font-normal line-through decoration-sale"
PRICE_CLASS = "flex flex-row items-center gap-2 text-sm leading-tight 3xl:text-base"


def get_urls() -> list[str]:
    return [BASE_URL + f"?page={str(i + 1)}" for i in range(NUM_PAGES)]


def scrape_page(html_source: str) -> list[product.Product]:
    """Scrape the products from a page"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the products div
    products_div = soup.find("section", class_="grid")

    products = []

    # Loop through the products
    for product_element in products_div.find_all("article", class_=True):  # type: ignore # None possible
        # get name
        parent_name = product_element.find("span", class_=NAME_CLASS_PARENT)
        name = product_element.find("span", class_=NAME_CLASS)
        name = parent_name.text + " " + name.text if parent_name else name.text
        name = product.parse_str(name)

        price = product_element.find("span", class_=PRICE_CLASS)
        wo_discount = product_element.find("span", class_=PRICE_WO_DISCOUNT_CLASS)
        price = wo_discount.text if wo_discount else price.text
        price = product.parse_price(price)

        link = product_element.find("a", href=True)["href"]
        link = product.parse_str("https://plnts.com" + link)

        # Add the product to the list
        products.append(product.Product(name, None, price, link))

    return products
