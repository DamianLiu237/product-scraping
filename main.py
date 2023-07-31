import time

import pandas as pd
from sqlalchemy import create_engine
import requests

from web_scraping import (
    db,
    get_modules,
    scrape_products_parallel,
    scrape_products_selenium,
)


def update_db() -> pd.DataFrame:
    from scrapers import marktplaats

    engine = create_engine("sqlite:///competitors.db")
    existing_data_df = pd.read_sql_table("products_data", con=engine)

    # Convert 'timestamp' column to datetime format
    existing_data_df["scraped_on"] = pd.to_datetime(existing_data_df["scraped_on"])

    existing_data_df = existing_data_df[existing_data_df["website"] == "marktplaats"]

    # Dummy data for the new dataframe
    new_data_df = scrape_products_parallel({"marktplaats": marktplaats})  # type: ignore

    # Convert 'timestamp' column to datetime format
    new_data_df["scraped_on"] = pd.to_datetime(new_data_df["scraped_on"])

    print("Existing Data:")
    print(existing_data_df)
    print("\nNew Data:")
    print(new_data_df)

    # Step 1: Merge the new dataframe with the existing data using pd.concat():
    merged_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)

    # Step 2: Sort the merged dataframe by 'timestamp' in descending order:
    merged_df.sort_values(by="scraped_on", ascending=False, inplace=True)

    # Step 3: Remove duplicates keeping the latest occurrence based on 'product_name':
    merged_df.drop_duplicates(
        subset=[i for i in merged_df.columns if i != "scraped_on"],
        keep="first",
        inplace=True,
    )

    # Step 4: Reset the index of the merged dataframe:
    merged_df.reset_index(drop=True, inplace=True)

    print("\nMerged Data with Latest Timestamps:")
    print(merged_df)

    return merged_df


def main() -> None:
    # parallel_modules = get_modules("parallel_modules")
    # selenium_modules = get_modules("selenium_modules")

    # a = time.perf_counter()
    # parallel_results = scrape_products_parallel(parallel_modules)
    # selenium_results = scrape_products_selenium(selenium_modules)
    # print(f"Time taken: {time.perf_counter() - a:.2f} seconds")
    # merged_df = update_db()
    # merged_df.to_csv("test.csv", index=False)

    # print(merged_df)

    # df = pd.read_csv("test.csv")
    # print(df)

    # db.delete_website("marktplaats")
    # db.add_to_db(df)

    # merged_df.to_csv("test.csv", index=False)

    from scrapers import plantique

    new_data_df = scrape_products_parallel({"plantique": plantique})

    new_data_df.drop_duplicates(
        subset=[i for i in new_data_df.columns if i != "scraped_on"],
        keep="first",
        inplace=True,
    )

    print(new_data_df)
    db.delete_website("plantique")
    db.add_to_db(new_data_df)

    # res = requests.get("https://plantique.shop/collections/alle-planten?page=8")

    # print(res.text)


if __name__ == "__main__":
    main()
