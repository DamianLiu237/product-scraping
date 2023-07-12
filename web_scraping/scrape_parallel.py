import asyncio
from typing import Callable

import pandas as pd

from .fetch import send_async_request
from .product import Product
from .scrape_utils import Website, convert_to_df, flatten_list

Scraper = Callable[[str], list[Product]]


async def scrape_products_page(url: str, scrape_fn: Scraper) -> list[Product]:
    html_source = ""

    try:
        html_source = await send_async_request(url)
    except Exception as e:
        print("Error fetching page at: ", url)
        print(e)

    try:
        return scrape_fn(html_source)

    except AttributeError as e:
        print("Error scraping page at: ", url)
        print(e)

        return []


async def scrape_products_website(website_name: str, website: Website) -> pd.DataFrame:
    coros = []
    for url in website.get_urls():
        coros.append(scrape_products_page(url, website.scrape_page))
    results = await asyncio.gather(*coros)
    results = flatten_list(results)

    return convert_to_df(website_name, results)


async def products_websites_parallel(websites: dict[str, Website]) -> pd.DataFrame:
    coros = []
    for website_name, website in websites.items():
        coros.append(scrape_products_website(website_name, website))

    websites_dfs = await asyncio.gather(*coros)

    return pd.concat(websites_dfs, ignore_index=True)


def products_websites_sync(websites: dict[str, Website]) -> pd.DataFrame:
    return asyncio.run(products_websites_parallel(websites))
