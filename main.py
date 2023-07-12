import time

from web_scraping import (
    get_modules,
    scrape_products_parallel,
    scrape_products_selenium,
)


def main() -> None:
    parallel_modules = get_modules("parallel_modules")
    selenium_modules = get_modules("selenium_modules")

    a = time.perf_counter()
    parallel_results = scrape_products_parallel(parallel_modules)
    selenium_results = scrape_products_selenium(selenium_modules)
    print(f"Time taken: {time.perf_counter() - a:.2f} seconds")

    # from scrapers import casa_botanica

    # res = scrape_products_parallel({"casa_botanica": casa_botanica})
    # print(res)
    # db.delete_website("casa_boptanica")
    # db.add_to_db(res)\


if __name__ == "__main__":
    main()
