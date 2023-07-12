import importlib
import itertools
import json
from typing import Protocol

import pandas as pd

from .product import Product

# TODO: put in config file
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


class Website(Protocol):
    def get_urls(self) -> list[str]:
        ...

    def scrape_page(self, page: str) -> list[Product]:
        ...


def flatten_list(lst: list[list]) -> list:
    return list(itertools.chain.from_iterable(lst))


def convert_to_df(website_name: str, products: list[Product]) -> pd.DataFrame:
    df = pd.DataFrame(products)
    df.drop_duplicates(keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["scraped_on"] = pd.Timestamp.now().strftime(TIME_FORMAT)
    df["website"] = website_name

    return df


def get_modules(key: str) -> dict[str, Website]:
    with open("product_scraper/scrapers.json", "r") as f:
        module_names = json.load(f)

    modules = {}
    for module_name in module_names[key]:
        path = "scrapers." + module_name
        modules[module_name] = importlib.import_module(path)

    return modules
