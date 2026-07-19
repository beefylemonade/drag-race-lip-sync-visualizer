from enum import Enum
from models import SeasonType


class Franchise(Enum):

    # Regular season (regular)
    US = (18,SeasonType.REGULAR, "RuPaul's Drag Race", "RuPaul's Drag Race (Season {})")
    UK = (7,SeasonType.REGULAR, "RuPaul's Drag Race UK", "RuPaul's Drag Race UK (Season {})")
    CA = (7,SeasonType.REGULAR, "Drag Race Canada", "")
    # ...

    # All-stars (all_stars)
    AS_US = (
        11, SeasonType.ALL_STARS,
        "RuPaul's Drag Race All Stars",
        "RuPaul's Drag Race All Stars (Season {})",
    )

    # VS The world "vs_the_world"

    # Special Season
    # AS_GLOBAL "global"
    # AS_ROYAL "royal"

    def __init__(self, number_of_season, season_type, title, page_name):
        self.number_of_season = number_of_season
        self.season_type = season_type
        self.title = title
        self.page_name = page_name


WIKI_URL = "https://rupaulsdragrace.fandom.com/api.php"
