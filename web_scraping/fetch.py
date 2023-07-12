import aiohttp
import httpx
from selenium import webdriver

# TODO: put in config file
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
HTTPX_TIMEOUT = 120


async def send_async_request(url: str) -> str:
    """Get the HTML content from the website using requests"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status not in (200, 201, 202):
                print(f"~~~ \n REQUEST FAILED AT: {url}, \n {response.status} \n ~~~")

            html_source = await response.text()

    return html_source
