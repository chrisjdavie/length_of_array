"""
Utils for support of simple scraping
"""
from asyncio import run
from pathlib import Path
import pickle

from aiohttp import ClientSession

from simple_scraper.parsers import parse_html
from simple_scraper.run_scraper import get_html
from simple_scraper.tests import data


async def save_new_data():
    target_url = "https://www.bbc.co.uk/sport/mixed-martial-arts/46168948"

    output_path = Path(data.__path__[0] + "/bbc_news.p")

    async with ClientSession() as session:
        html = await get_html(target_url, session)

    site_data = parse_html(target_url, html)
    print(site_data)
    for image in site_data.images:
        print(image)

#     with output_path.open("wb") as output_fh:
#         pickle.dump(html, output_fh)


if __name__ == "__main__":
    run(save_new_data())
