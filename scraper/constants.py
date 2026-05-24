from enum import Enum

class Franchise(Enum):

    # Regular season
    US          = ("US", 18, "RuPaul's Drag Race (Season {})")
    UK          = ("UK", 7, "RuPaul's Drag Race UK (Season {})")
    CANADA      = ("CA", 7, "")
    #...

    # All-stars
    AS_US        = ("AS_US",11, "RuPaul's Drag Race All Stars (Season {})")

    # VS The world

    # Special Season

    def __init__(self, abbr, number_of_season, page_name):
        self.abbr         = abbr
        self.number_of_season = number_of_season
        self.page_name      = page_name

WIKI_URL = "https://rupaulsdragrace.fandom.com/api.php"