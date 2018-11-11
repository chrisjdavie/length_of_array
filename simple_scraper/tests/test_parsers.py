"""
Testing the parsers on saved html from previous web requests
"""
import pickle

from asynctest import TestCase
from parameterized import parameterized

from simple_scraper.parsers import ImageParser, parse_html, TitleParser
from simple_scraper.tests.data.website_results import PARAMETERIZED_SITEDATA


class CheckParser(TestCase):

    _parser_class = None

    def _check_parser(self, path, expected, check_fn):

        with path.open("rb") as fh:
            html = pickle.load(fh)

        parser = self._parser_class()
        parser.feed(html)

        actual = check_fn(parser)
        self.assertEqual(expected, actual)


def custom_name_func(testcase_func, _, param):
    return f"{testcase_func.__name__}_{param[0][0].stem}"


class TestTitleParser(CheckParser):

    _parser_class = TitleParser

    def check_parser(self, path, expected_headline):

        def check_fn(parser):
            return parser.headline

        self._check_parser(path, expected_headline, check_fn)

    @parameterized.expand(PARAMETERIZED_SITEDATA,
                          testcaset_func_name=custom_name_func)
    def test(self, path, sitedata):
        self.check_parser(path, sitedata.headline)


class TestImageParser(CheckParser):

    _parser_class = ImageParser

    def check_parser(self, path, expected_image_data):

        def check_fn(parser):
            return sorted(parser.images, key=lambda x: x.url)

        return self._check_parser(path, expected_image_data, check_fn)

    @parameterized.expand(PARAMETERIZED_SITEDATA,
                          testcase_func_name=custom_name_func)
    def test(self, path, sitedata):
        self.check_parser(path, sorted(sitedata.images, key=lambda x: x.url))


class TestParseHtml(TestCase):

    def test_returns_none_with_no_headline(self):
        self.assertIsNone(parse_html("", ""))
