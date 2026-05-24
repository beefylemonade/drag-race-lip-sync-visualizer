import requests
from constants import Franchise
import constants


def get_section_index (franchise: Franchise, season_number: int, section_name: str) -> str | None:
    params = {
        "action": "parse",
        "page": franchise.page_name.format(season_number),
        "prop": "sections",
        "format": "json"
    }

    
    response = requests.get(
        constants.WIKI_URL,
        params=params
    )
    data = response.json()
    sections = data["parse"]["sections"]

    for section in sections:
        
        if section_name.lower() in section["line"].lower():
            return int(section["index"])

    return None



def get_content(franchise: Franchise, season_number: int, section_name: str) -> str | None:
    index = get_section_index(franchise, season_number, section_name)

    if index is None:

        print(f'Season {season_number} does not contain {section_name}')
        return
    
    params = {
            "action": "parse",
            "page": franchise.page_name.format(season_number),
            "prop": "wikitext",
            "section": index,
            "format": "json"
        }

    response = requests.get(
            constants.WIKI_URL,
            params=params
        )

    data = response.json()

    return data["parse"]["wikitext"]["*"]

print(get_content(Franchise.AS_US, 7, "Contestants"))
#f = Franchise.US
#print(f.page_name.format(8))