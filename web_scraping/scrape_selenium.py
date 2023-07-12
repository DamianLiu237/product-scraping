from functools import lru_cache
from typing import Callable

import pandas as pd
from selenium import webdriver

from .product import Product
from .scrape_utils import Website, convert_to_df, flatten_list

# TODO: put in config file
CHROME_PATH = "C:\\Program Files (x86)\\chromedriver.exe"

Scraper = Callable[[str], list[Product]]


@lru_cache(maxsize=1)
def _create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    return webdriver.Chrome(CHROME_PATH, options=options)


def scrape_products_page(url: str, scrape_fn: Scraper) -> list[Product]:
    driver = _create_driver()
    html_source = ""

    try:
        html_source = driver.get(url)
        html_source = driver.page_source
    except Exception as e:
        print("Error fetching page at: ", url)
        print(e)

    try:
        return scrape_fn(html_source)

    except AttributeError as e:
        print("Error scraping page at: ", url)
        print(e)

        return []


def scrape_products_website(website_name: str, website: Website) -> pd.DataFrame:
    products = []
    for url in website.get_urls():
        products.append(scrape_products_page(url, website.scrape_page))

    return convert_to_df(website_name, flatten_list(products))


def products_websites_selenium(websites: dict[str, Website]) -> pd.DataFrame:
    """Scrape the products from all websites using Selenium"""

    dfs = []
    for website_name, website in websites.items():
        dfs.append(scrape_products_website(website_name, website))

    return pd.concat(dfs, ignore_index=True)
