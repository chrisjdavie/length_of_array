"""
Data models of the scraper results
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ImageData:
    """Url and caption of the image data

    Frozen so it can be put in a set."""
    url: str
    caption: str


@dataclass
class SiteData:
    """Url, headline and list of images for a give URL"""
    url: str
    headline: str
    images: List[ImageData]
