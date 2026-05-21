import requests


def get_section_index (season_number: int, section_name: str) -> str | None:
    params = {
        "action": "parse",
        "page": f"RuPaul's Drag Race (Season {season_number})",
        "prop": "sections",
        "format": "json"
    }

    response = requests.get(
        "https://rupaulsdragrace.fandom.com/api.php",
        params=params
    )
    data = response.json()
    sections = data["parse"]["sections"]

    for section in sections:
        
        if section_name.lower() in section["line"].lower():
            return int(section["index"])

    return None


season_number = 18

index = get_section_index(season_number, "Contestants")


params = {
        "action": "parse",
        "page": f"RuPaul's Drag Race (Season {season_number})",
        "prop": "wikitext",
        "section": index,
        "format": "json"
    }

response = requests.get(
        "https://rupaulsdragrace.fandom.com/api.php",
        params=params
    )

data = response.json()
print(data["parse"]["wikitext"]["*"])