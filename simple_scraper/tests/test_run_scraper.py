import pickle

from asynctest import TestCase

from simple_scraper.run_scraper import ImageTitleParser, run, SiteData, \
    ImageData


class TestRun(TestCase):

    async def test(self):

        urls = ["http://www.skysports.com/football/news/11661/10871659/who-won-your-clubs-player-of-the-year-award",
                "http://www.bbc.co.uk/sport/tennis/37268846",
                "https://www.theguardian.com/us-news/2018/nov/08/california-borderline-mass-shooting-thousand-oaks"]

        results = await run(urls)

        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIsInstance(res, SiteData)
        # TODO - this needs to spoof the results of the above site, and then
        #        spoof the results of the code (potentially)


class TestImageTitleParser(TestCase):

    _placeholder_url = "ABC"

    def check_parser(self, fpath, expected_site_data):

        with open(fpath, "rb") as fh:
            html = pickle.load(fh)

        parser = ImageTitleParser()
        parser.feed(html)

        site_data = parser.build_site_data(self._placeholder_url)
        self.assertEqual(expected_site_data, site_data)

    def test_bbc(self):

        fpath = "simple_scraper/data/bbc_sport.p"

        expected_site_data = SiteData(
            self._placeholder_url,
            "US Open 2016: Novak Djokovic beats Kyle Edmund in fourth round",
            set([
                ImageData(
                    "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/1171C/production/_91025417_edmund_groan_getty.jpg",
                    "Edmund was unable to make much of an impression against Djokovic"),
                ImageData(
                    "https://ichef.bbci.co.uk/onesport/cps/{width}{hidpi}/cpsprodpb/0994/production/_91025420_djokovic_afp.jpg",
                    "Djokovic kept Edmund moving around the court"),
            ])
        )
        self.check_parser(fpath, expected_site_data)

    def test_sky(self):

        fpath = "simple_scraper/data/sky_football.p"

        expected_site_data = SiteData(
            self._placeholder_url,
            "Callum Wilson called up to England's 28-man squad for USA, Croatia games",
            set([
                ImageData(
                    "https://e2.365dm.com/18/10/768x432/skysports-callum-wilson-bournemouth_4466759.jpg?20181027165135",
                    "Callum Wilson has received his first England call-up"),
                ImageData(
                    "https://e2.365dm.com/18/09/768x432/skysports-dele-alli-tottenham_4434755.jpg?20180927073333",
                    "Dele Alli is back in the England squad after injury"),
            ])
        )
        self.check_parser(fpath, expected_site_data)

    def test_guardian(self):

        fpath = "simple_scraper/data/guardian.p"

        expected_site_data = SiteData(
            self._placeholder_url,
            "Thousand Oaks shooting: gunman kills 12 at California western bar",
            set([
                ImageData(
                    "https://i.guim.co.uk/img/media/93c73bb5570f220c9cc794b07dfb9a752a4a9a84/0_892_4200_2519/master/4200.jpg?width=300&quality=85&auto=format&fit=max&s=2a632bf46cdac89b326e6d9aaf8ec3c3",
                    "Women who fled from the shooting at the Borderline Bar and Grill. Photograph: Mike Nelson/EPA"),
            ])
        )
        self.check_parser(fpath, expected_site_data)
