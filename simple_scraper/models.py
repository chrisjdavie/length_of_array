"""
Data models of the scraper results
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ImageData:

    url: str
    caption: str


@dataclass
class SiteData:

    url: str
    headline: str
    images: List[ImageData]
