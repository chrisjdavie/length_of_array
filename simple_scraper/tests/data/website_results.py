from pathlib import Path

from simple_scraper.models import ImageData, SiteData

DATA_DIR = Path(__file__).parent

BBC_SPORTS_PATH = DATA_DIR.joinpath(Path("bbc_sport.p"))
BBC_SPORTS_SITE_DATA = SiteData(
    "http://www.bbc.co.uk/sport/tennis/37268846",
    "US Open 2016: Novak Djokovic beats Kyle Edmund in fourth round",
    [
        ImageData(
            "https://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb/1171C/production/_91025417_edmund_groan_getty.jpg",
            "Edmund was unable to make much of an impression against Djokovic"),
        ImageData(
            "https://ichef.bbci.co.uk/onesport/cps/976/cpsprodpb/0994/production/_91025420_djokovic_afp.jpg",
            "Djokovic kept Edmund moving around the court"),
    ]
)

SKY_0_PATH = DATA_DIR.joinpath(Path("sky_football_0.p"))
SKY_0_SITE_DATA = SiteData(
    "http://www.skysports.com/football/news/11661/10871659/who-won-your-clubs-player-of-the-year-award",
    "Callum Wilson called up to England's 28-man squad for USA, Croatia games",
    [
        ImageData(
            "https://e2.365dm.com/18/10/768x432/skysports-callum-wilson-bournemouth_4466759.jpg?20181027165135",
            "Callum Wilson has received his first England call-up"),
        ImageData(
            "https://e2.365dm.com/18/09/768x432/skysports-dele-alli-tottenham_4434755.jpg?20180927073333",
            "Dele Alli is back in the England squad after injury"),
    ]
)

SKY_1_PATH = DATA_DIR.joinpath(Path("sky_football_1.p"))
SKY_1_SITE_DATA = SiteData(
    "https://www.skysports.com/football/news/12016/11548074/callum-wilson-called-up-to-englands-28-man-squad-for-usa-croatia-games",
    "Who won your club's Player of the Year award?",
    [
        ImageData(
            "https://e1.365dm.com/17/04/768x432/skysports-ngolo-kante-chelsea-pfa-award_3937274.jpg?20170423234739",
            "N'Golo Kante with the PFA Players' Player of the Year award"),
        ImageData(
            "https://e1.365dm.com/17/01/768x432/skysports-lee-grant-stoke-city-premier-league_3864089.jpg?20170103210810",
            "Lee Grant won both the Stoke Fans' and Players' Player of the Year awards"),
        ImageData(
            "https://e1.365dm.com/17/05/768x432/skysports-tom-davies-romelu-lukaku-everton_3949965.jpg?20170510171154",
            "Romelu Lukaku and Tom Davies landed the big awards at Goodison Park"),
        ImageData(
            "https://e1.365dm.com/16/12/768x432/skysports-sadio-mane-liverpool-premier-league_3860203.jpg?20161228114105",
            "Mane claimed two awards at Liverpool after his scintillating debut season"),
        ImageData(
            "https://e2.365dm.com/17/02/768x432/skysports-gylfi-sigurdssson-swansea-manchester-man-city_3885319.jpg?20170205152836",
            "Gylfi Sigurdsson scooped two awards for Swansea"),
        ImageData(
            "https://e1.365dm.com/17/03/768x432/skysports-sam-clucas-hull-leicester_3902859.jpg?20170819182810",
            "Clucas scooped Hull's Player of the Year Award, selected by manager Marco Silva"),
        ImageData(
            "https://e0.365dm.com/17/05/768x432/skysports-leicester-kasper-schmeichel-watford_3948414.jpg?20170508165747",
            "Kasper Schmeichel scooped an awards double for Leicester"),
        ImageData(
            "https://e1.365dm.com/17/05/768x432/skysports-manchester-united-david-de-gea-ander-herrera_3957343.jpg?20170518232326",
            "David de Gea presented Ander Herrera with the Sir Matt Busby Player of the Year award"),
        ImageData(
            "https://e0.365dm.com/17/01/768x432/skysports-oriol-romeu-southampton_3876652.jpg?20170123171850",
            "It was a clean sweep for Southampton's engine in midfield, Oriol Romeu"),
        ImageData(
            "https://e1.365dm.com/17/04/768x432/skysports-dele-alli-tottenham-young-player-of-the-year_3937279.jpg?20170424001748",
            "Tottenham Dele Alli with the PFA Young Player of the Year award")
    ]
)

GUARDIAN_PATH = DATA_DIR.joinpath(Path("guardian.p"))
GUARDIAN_SITE_DATA = SiteData(
    "https://www.theguardian.com/us-news/2018/nov/08/california-borderline-mass-shooting-thousand-oaks",
    "Thousand Oaks shooting: gunman kills 12 at California western bar",
    [
        ImageData(
            "https://i.guim.co.uk/img/media/93c73bb5570f220c9cc794b07dfb9a752a4a9a84/0_892_4200_2519/master/4200.jpg?width=300&quality=85&auto=format&fit=max&s=2a632bf46cdac89b326e6d9aaf8ec3c3",
            "Women who fled from the shooting at the Borderline Bar and Grill. Photograph: Mike Nelson/EPA")
    ]
)

PARAMETERIZED_SITEDATA = [
    (BBC_SPORTS_PATH, BBC_SPORTS_SITE_DATA),
    (SKY_0_PATH, SKY_0_SITE_DATA),
    (SKY_1_PATH, SKY_1_SITE_DATA),
    (GUARDIAN_PATH, GUARDIAN_SITE_DATA)]
