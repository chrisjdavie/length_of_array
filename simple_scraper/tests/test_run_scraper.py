"""
Various forms of integration tests on the scraper runners, with the web
requests stubbed out.

Also some unit tests for stability of the connetion
"""
from contextlib import asynccontextmanager
import json
import logging
import os
from pathlib import Path
import pickle
from tempfile import NamedTemporaryFile

from aiohttp.client_exceptions import InvalidURL
from asynctest import TestCase, patch, strict
from asynctest.mock import MagicMock, CoroutineMock

from simple_scraper.models import SiteData
from simple_scraper.run_scraper import get_html, logger, run, run_from_stdin
from simple_scraper.tests.data.website_results import PARAMETERIZED_SITEDATA

logger.setLevel(logging.WARNING)

RUN_SCRAPER = "simple_scraper.run_scraper"
RUN_SCRAPER_CLIENT_SESSION = RUN_SCRAPER + ".ClientSession"


class StubResponse:
    """Stub of an aiohttp repsonse"""

    def __init__(self, url):
        self._url = url

    async def text(self):
        for path, sitedata in PARAMETERIZED_SITEDATA:
            if sitedata.url == self._url:
                with path.open("rb") as data_fh:
                    return pickle.load(data_fh)


class StubSession:
    """Stub of an aiohttp Session"""

    @asynccontextmanager
    async def get(self, url):
        yield StubResponse(url)


@asynccontextmanager
async def stub_client_session():
    """Stub of aiohttp.ClientSession"""
    yield StubSession()


class TestRunFromStdin(TestCase):
    """
    Simulates being run from the commandline.

    python simple_scraper/run_scraper.py [filename] < [list of urls]

    Mocks out stdin and argvs to achieve desired effect. Checks output file is
    created, and that it's a json.
    """

    @patch(RUN_SCRAPER_CLIENT_SESSION, new=stub_client_session)
    @strict
    async def test(self):

        def stub_stdin():
            for _, site_data in PARAMETERIZED_SITEDATA:
                yield site_data.url

        # generate a unique name that doesn't exist on the filesystem
        with NamedTemporaryFile() as tmp:
            pass

        stub_argv = ["", tmp.name]

        with patch(RUN_SCRAPER + ".stdin", new=stub_stdin()):
            with patch(RUN_SCRAPER + ".argv", stub_argv):
                await run_from_stdin()

        # check file exists
        self.assertTrue(os.path.exists(tmp.name))
        # check it can be loaded
        with Path(tmp.name).open("r") as tmp_fh:
            json.load(tmp_fh)

        os.remove(tmp.name)


class TestRun(TestCase):

    @patch(RUN_SCRAPER_CLIENT_SESSION, new=stub_client_session)
    @strict
    async def test(self):

        urls = [site_data.url for _, site_data in PARAMETERIZED_SITEDATA]

        results = await run(urls)

        self.assertEqual(len(results), len(PARAMETERIZED_SITEDATA))
        for res in results:
            self.assertIsInstance(res, SiteData)


class TestGetHtml(TestCase):
    """
    Unit tests on get_html (mainly stability, as this is where the url and
    connection failures get tripped)
    """

    async def setUp(self):

        # mock out responses
        self.mock_response = MagicMock()
        self.mock_response.text = CoroutineMock()

        @asynccontextmanager
        async def get(*args, **kwargs):
            yield self.mock_response

        self.mock_session = MagicMock()
        self.mock_session.get = get

    @strict
    async def test_gets_text(self):

        await get_html("", self.mock_session)

        self.mock_response.text.assert_awaited_once()

    @strict
    async def test_asks_for_utf8_on_unidecode_error(self):

        expected_html = "ABCD"
        self.mock_response.text.side_effect = [
            UnicodeDecodeError("", b"", 0, 0, ""), expected_html]

        html = await get_html("", self.mock_session)

        self.assertEqual(expected_html, html)
        # called once with the error, once without
        self.assertEqual(self.mock_response.text.await_count, 2)
        self.mock_response.text.assert_awaited_with("utf-8")

    @strict
    async def test_invalid_url_logs_recovers(self):

        @asynccontextmanager
        async def get(url):
            raise InvalidURL(url)
            yield

        self.mock_session.get = get

        with self.assertLogs(logger, logging.ERROR):
            result = await get_html("", self.mock_session)
        self.assertEqual(result, "")
