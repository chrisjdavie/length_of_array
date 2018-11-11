"""
Parse the website html for images and headlines.

This is using separate parsers for both the images and headlines - if this
becomes expensive, it's very straightforwards to have a single parser that
goes through the other parsers calling their methods on the tags and data.
It wasn't the slow part of this (waiting for the website response was) so I've
not implemented it.
"""
from html.parser import HTMLParser
from typing import Optional

from simple_scraper.models import ImageData, SiteData


def parse_html(url: str, html: str) -> Optional[SiteData]:
    """
    Run the parsers on the html, construct desired data
    """

    image_parser = ImageParser()
    image_parser.feed(html)
    title_parser = TitleParser()
    title_parser.feed(html)
    if title_parser.headline:
        return SiteData(url, title_parser.headline, image_parser.images)
    return None


class ImageParser(HTMLParser):
    """
    Scrapes the images from the html when the image has a caption.

    Finds the image tage, searches nearby for the caption, if the caption is
    found saves the ImageData. If a caption isn't found nearby, it abandons the
    image.
    """

    # bbc has some stock captions that hide the real captions
    _invalid_captions = [
        "Media caption",
        "Image copyright",
        "Media playback is unsupported on your device",
        "Image caption"]

    def __init__(self, *args, **kwargs):

        # set as this sometime finds duplicate images
        self._images = set()

        self._image_url = ""
        self._caption = ""
        self._image_start = False
        self._caption_dist = 0
        # maximum distance captions can be from the image - 50 is found to work,
        # but is trial and error
        self._max_caption_dist = 50

        self._caption_tag = ""
        self._caption_start = False

        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        # This assumes that the caption follows the image in the website code
        # without another image inbetween. This is perhaps assuming people think
        # about code in the way I do, but that's not always true.

        # flag if image, grab the url
        if tag == "img":
            # start search for caption
            self._caption_dist = 0
            self._image_start = True
            self._caption_start = False
            # look for website url
            for attr in attrs:
                if "http" in attr[1] and not " " in attr[1]:
                    self._image_url = attr[1]
                    # BBC has some odd resolution behaviour in URLs
                    if "{width}{hidpi}" in self._image_url:
                        self._image_url = self._image_url.replace(
                            "{width}{hidpi}", "976")

        # if an image has been found, see if the is the associated caption
        # tag. If it is, record the tag and flag. Otherwise, check that the
        # code it's too far from the image to be a caption.
        if self._image_start:
            for pair in attrs:
                for single in pair:
                    if isinstance(single, str) and "caption" in single:
                        # start data search for caption
                        self._caption_tag = tag
                        self._caption_start = True
                        break
                else:
                    self._caption_dist += 1
                    if self._caption_dist > self._max_caption_dist:
                        self._image_start = False

    def handle_data(self, data):
        if self._caption_start:
            if data.strip():
                if data.strip() not in self._invalid_captions:
                    # found caption - build image, stop image and caption
                    # search
                    self._images.add(ImageData(self._image_url, data.strip()))
                    self._caption_start = False
                    self._image_start = False

    def handle_endtag(self, tag):
        if tag == self._caption_tag and self._caption_start:
            # end data search for caption
            self._caption_start = False

    @property
    def images(self):
        """Returns a list of found images"""
        return list(self._images)


class TitleParser(HTMLParser):
    """
    Searches for the 'h1' tag. Once it finds it, it looks for the data stored
    within it.
    """

    def __init__(self, *args, **kwargs):

        self.headline = None
        self._headline_start = False

        super().__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self._headline_start = True

    def handle_data(self, data):
        if self._headline_start:
            if data.strip():
                self.headline = data.strip()
                self._headline_start = False

    def handle_endtag(self, tag):
        if tag == "h1" and self._headline_start:
            self._headline_start = False
