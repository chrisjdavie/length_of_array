"""
Runners for the url scrapers.

Scrapes provided urls for headlines and images, and handles the output.
"""
from asyncio import run as asyncio_run, create_task, sleep
from dataclasses import asdict
import json
import logging
from pathlib import Path
from sys import argv, stdin
from typing import Generator, Iterable, List, Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError, InvalidURL

from simple_scraper.models import SiteData
from simple_scraper.parsers import parse_html

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

# limit the number of concurrent scrapers
SIMULTANEOUS_SCRAPERS_LIMIT = 100


async def run_from_stdin() -> None:
    """Runs from stdin.

    Expects the output path as the first argument, and
    urls separated with new lines as the input from stdin.

    Terminates on the end of the stdin or on an empty line.

    On termination of stdin and conclusion of the scraping, it writes the
    results as a json to the output path."""

    def terminate_stdin_on_empty_line() -> Generator[str, None, None]:
        for line in stdin:
            if not line.strip():
                break
            yield line.strip()

    results = await run(terminate_stdin_on_empty_line())

    with Path(argv[1]).open("w") as json_fh:
        json.dump(transform(results), json_fh, indent=4)


async def run(all_urls: Iterable[str]) -> List[SiteData]:
    """Runs the scraper on the 'all_urls' iterable.

    Launches each url as a separate async task. Limits the number of
    simultaneous scrapers to SIMULTANEOUS_SCRAPERS_LIMIT.

    all_urls should return valid urls (otherwise it won't be able to scrape
    them)"""

    async with ClientSession() as session:

        # launch scraping tasks
        tasks = []
        for url in all_urls:
            tasks.append(create_task(scrape_url(url, session)))
            await sleep(0)
            # limit the number of simultaneous urls being scraped

            while (len(tasks) - sum([task.done() for task in tasks])
                   >= SIMULTANEOUS_SCRAPERS_LIMIT):
                await sleep(0.1)

        # wait for scraping tasks to complete
        tasks_done = [task.done() for task in tasks]
        while not all(tasks_done):
            logger.debug("%i/%i urls scraped", sum(tasks_done), len(tasks))
            await sleep(0.1)
            tasks_done = [task.done() for task in tasks]

    # return the results of the scraping tasks
    return [task.result() for task in tasks if task.result()]


async def scrape_url(url: str, session: ClientSession) -> Optional[SiteData]:
    """Run the scraping for an individual url"""
    logger.info(f"Started downloading {url}")
    html = await get_html(url, session)
    logger.info(f"Parsing {url}")
    site_data = parse_html(url, html)
    logger.info(f"Finished {url}")
    return site_data


async def get_html(url: str, session: ClientSession) -> str:
    """
    Get html from a url.

    Catches invalid URL and connection errors, logs the error and returns an
    empty string.
    """
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
        logger.exception("Invalid URL %s", url)
    except ClientError:
        logger.exception("Connection Error")
    return ""


def transform(results: List[SiteData]) -> list:
    """Transforms a list of sitedata to something compatible with jsons for
    output.

    Composed of lists, dictionaries, strings and integers."""
    return [asdict(res) for res in results]


if __name__ == "__main__":
    print("Please type in the urls to scrape and press enter. An empty line "
          "will terminate the input and trigger writing to the json.")
    asyncio_run(run_from_stdin())
