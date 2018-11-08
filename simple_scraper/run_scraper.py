from asyncio import run as asyncio_run, sleep
from dataclasses import dataclass
from html.parser import HTMLParser
from sys import stdin
from typing import List, Set

import aiohttp


class ImageTitleParser(HTMLParser):

    def __init__(self):

        self._images = set()
        self._headline = ""
        self._headline_start = False

        self._image_url = ""
        self._caption = ""
        self._image_start = False
        self._caption_dist = 0
        # maximum distance captions can be from the image - 50 is found to work,
        # but is trial and error
        self._max_caption_dist = 50

        self._caption_tag = ""
        self._caption_start = False

        super().__init__()

    def handle_starttag(self, tag, attrs):

        if tag == "img":
            self._image_start = True
            for attr in attrs:
                if "http" in attr[1] and not " " in attr[1]:
                    self._image_url = attr[1]

        if self._image_start:
            for pair in attrs:
                for single in pair:
                    if isinstance(single, str) and "caption" in single:
                        self._caption_tag = tag
                        self._caption_start = True
                else:
                    self._caption_dist += 1
                    if self._caption_dist > self._max_caption_dist:
                        self._image_start = False
                        self._caption_dist = 0

        if tag == "h1":
            self._headline_start = True

    def handle_data(self, data):
        if self._caption_start:
            if data.strip():
                self._images.add(ImageData(self._image_url, data.strip()))
                self._caption_start = False

        if self._headline_start:
            if data.strip():
                self._headline = data.strip()
                self._headline_start = False

    def handle_endtag(self, tag):
        if tag == "h1" and self._headline_start:
            self._headline_start = False
        if tag == self._caption_tag and self._caption_start:
            self._caption_start = False
            self._image_start = False

    def build_site_data(self, url):
        return SiteData(url, self._headline, self._images)


@dataclass(frozen=True)
class ImageData:

    url: str
    caption: str


@dataclass
class SiteData:

    url: str
    headline: str
    images: Set[ImageData]


def extract_content(html):

    parser = ImageTitleParser()
    parser.feed(html)
    pass


async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def run(all_urls) -> List[SiteData]:
    for url in all_urls:
        print(url)
        await sleep(0)
    return []


async def run_from_file(fpath: str) -> List[SiteData]:

    with open(fpath, "r") as fhandle:
        return run(fhandle)


async def run_from_stdin() -> None:

    def terminate_stdin_on_empty_line():
        for line in stdin:
            if not line.strip():
                break
            yield line.strip()

    await run(terminate_stdin_on_empty_line())
    # todo - file write here


if __name__ == "__main__":
    asyncio_run(run_from_stdin())
