import asyncio
import re
from typing import Callable

import pandas as pd
from bs4 import BeautifulSoup

from .fetch import send_async_request

# TODO: Put in config file
TRUSTPILOT_URL = "https://www.trustpilot.com/review/"
SCORE_CLASS = "typography_heading-m__T_L_X typography_appearance-default__AAY17"
NUM_REVIEWS_CLASS = "typography_body-l__KUYFJ typography_appearance-default__AAY17"

Fetcher = Callable[[list[str]], list[str]]


def domain_from_url(url: str) -> str:
    """Get the domain from a URL"""
    string = r"(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)"

    return re.findall(string, url)[0]


def scrape_trustpilot_data(html_source: str) -> dict[str, float | int | str]:
    """Get the trustpilot data from a URL"""

    # Parse the HTML content
    soup = BeautifulSoup(html_source, "lxml")

    # Get the score
    score = soup.find("span", class_=SCORE_CLASS).text  # type: ignore

    # Get the number of reviews
    num_reviews = soup.find("p", class_=NUM_REVIEWS_CLASS).text  # type: ignore

    score = float(score)
    num_reviews = int(re.sub("[^0-9]", "", num_reviews))

    # Return the score and the number of reviews
    return {
        "trustpilot_score": score,
        "trustpilot_reviews": num_reviews,
    }


async def scrape_website_trustpilot(
    domain_url: str,
) -> dict[str, float | int | str | None]:
    domain_name = domain_from_url(domain_url)
    trustpilot_url = TRUSTPILOT_URL + domain_name

    try:
        html_source = await send_async_request(trustpilot_url)
        trustpilot_data = scrape_trustpilot_data(html_source)
    except Exception as e:
        print(f"Failed to scrape trustpilot data for {domain_name}: {e}")

        return {
            "trustpilot_score": None,
            "trustpilot_reviews": None,
            "id": None,
        }

    trustpilot_data["id"] = domain_name.split(".")[0]

    return trustpilot_data


async def trustpilot_data_async(domain_urls: list[str]) -> pd.DataFrame:
    """Fetch the HTML sources from a list of domain names and scrape the trustpilot data"""

    coros = [scrape_website_trustpilot(url) for url in domain_urls]
    result = await asyncio.gather(*coros)

    df = pd.DataFrame(result)
    df.set_index("id", inplace=True)
    df.dropna(inplace=True)

    return df


def trustpilot_data(domain_urls: list[str]) -> pd.DataFrame:
    return asyncio.run(trustpilot_data_async(domain_urls))

    # orig_df = pd.read_csv("plant_shops.csv")
    # orig_df.set_index("id", inplace=True)
    # # orig_df = orig_df.loc[["intratuin", "rimboe"]]

    # df = orig_df[orig_df["trustpilot_score"].isna()]
    # # df.loc["rimboe", "trustpilot_score"] = 5
    # # df.loc["rimboe", "trustpilot_reviews"] = 35

    # urls = df["url"].tolist()
    # trustpilot_df = trustpilot_data(urls)

    # orig_df.update(trustpilot_df)

    # print(trustpilot_df)
    # orig_df.to_csv("plant_shops1.csv")
