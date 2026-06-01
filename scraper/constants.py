from enum import Enum

class Franchise(Enum):

    # Regular season
    US          = (18,"RuPaul's Drag Race", "RuPaul's Drag Race (Season {})")
    UK          = (7,"RuPaul's Drag Race UK", "RuPaul's Drag Race UK (Season {})")
    CA          = (7,"Drag Race Canada", "")
    #...

    # All-stars
    AS_US        = (11,"RuPaul's Drag Race All Stars", "RuPaul's Drag Race All Stars (Season {})")

    # VS The world

    # Special Season

    def __init__(self, number_of_season,title, page_name):
        self.number_of_season = number_of_season
        self.title = title
        self.page_name = page_name

WIKI_URL = "https://rupaulsdragrace.fandom.com/api.php"