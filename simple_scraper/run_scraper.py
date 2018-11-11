from asyncio import run as asyncio_run, create_task, sleep
from dataclasses import asdict
import json
import logging
from pathlib import Path
from sys import argv, stdin
from typing import Generator, List

from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL, ClientError

from simple_scraper.models import SiteData
from simple_scraper.parsers import parse_html

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

# limit the number of concurrent scrapers
SIMULTANEOUS_SCRAPERS_LIMIT = 100


async def run_from_stdin() -> None:

    def terminate_stdin_on_empty_line() -> Generator:
        for line in stdin:
            if not line.strip():
                break
            yield line.strip()

    results = await run(terminate_stdin_on_empty_line())

    with Path(argv[1]).open("w") as json_fh:
        json.dump(transform(results), json_fh, indent=4)


async def run(all_urls) -> List[SiteData]:

    async with ClientSession() as session:

        # launch scraping tasks
        tasks = []
        for url in all_urls:
            tasks.append(create_task(scrape_url(url, session)))
            await sleep(0)
            # limit the number of simultaneous urls being scraped
            while (len(tasks) - sum([task.done() for task in tasks])
                    > SIMULTANEOUS_SCRAPERS_LIMIT):
                await sleep(1)

        # wait for scraping tasks to complete
        tasks_done = [task.done() for task in tasks]
        while not all(tasks_done):
            logger.debug(f"{sum(tasks_done)}/{len(tasks)} urls scraped")
            await sleep(1)
            tasks_done = [task.done() for task in tasks]

    # return the results of the scraping tasks
    return [task.result() for task in tasks if task.result()]


async def scrape_url(url: str, session: ClientSession):

    logger.info(f"Started downloading {url}")
    html = await get_html(url, session)
    logger.info(f"Parsing {url}")
    site_data = parse_html(url, html)
    logger.info(f"Finished {url}")
    return site_data


async def get_html(url: str, session: ClientSession) -> str:
    try:
        async with session.get(url) as response:
            try:
                return await response.text()
            except UnicodeDecodeError:
                # there is an issue with an underpinning library not always
                # decoding properly. Observed it decoding utf-8 as something
                # else
                return await response.text("utf-8")
    except InvalidURL:
        logger.exception(f"Invalid URL {url}")
    except ClientError:
        logger.exception("Connection Error")
    return ""


def transform(results: List[SiteData]) -> list:
    return [asdict(res) for res in results]


if __name__ == "__main__":
    print("Please type in the urls to scrape and press enter. An empty line "
          "will terminate the input and trigger writing to the json.")
    asyncio_run(run_from_stdin())
