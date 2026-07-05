import time
import requests
from pathlib import Path
from constants import Franchise
import constants as CONSTANTS

CACHE_LOCATION = Path("data/wiki_pages")
SLEEP_DURATION = 1.0
MAX_RETRIES    = 3


def polite_fetch_with_retry(url: str, params: dict, retry_count: int = MAX_RETRIES) -> requests.Response:
    """
    Make a GET request with exponential backoff on HTTP 429 responses.

    Args:
        url:         The endpoint URL.
        params:      Query parameters.
        retry_count: Maximum number of retry attempts.

    Returns:
        The successful response object.

    Raises:
        RuntimeError: If all retry attempts are exhausted.
    """
    for attempt in range(retry_count):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response

        elif response.status_code == 429:
            wait = 2 ** attempt 
            print(f"Rate limited. Waiting {wait}s before retry {attempt + 1}/{retry_count}...")
            time.sleep(wait)

        else:
            response.raise_for_status()  # raises an exception for 4xx/5xx errors

    raise RuntimeError(f"Failed to fetch after {retry_count} retries: {url}")


def get_section_index (franchise: Franchise, season_number: int, section_name: str) -> str | None:
    params = {
        "action": "parse",
        "page": franchise.page_name.format(season_number),
        "prop": "sections",
        "format": "json"
    }

    
    response = polite_fetch_with_retry(
        CONSTANTS.WIKI_URL,
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

    response = polite_fetch_with_retry(
            CONSTANTS.WIKI_URL,
            params=params
        )

    data = response.json()

    return data["parse"]["wikitext"]["*"]

# def legacy_fetch_wiki_page(franchise:str, season_number:int, use_cache:bool) -> str | None:

#     wiki_text = None
#     if use_cache:

#         try:
#             os.makedirs(CACHE_LOCATION, exist_ok=True)
#             print(f"Cache directory created or already exists: {CACHE_LOCATION}")
#         except OSError as e:
#             print(f"Error creating directory '{CACHE_LOCATION}': {e}")
#             use_cache = False # Disable error if fail to create directory for caching
    
#     if use_cache:
#         print("Caching enabled. Reading from local copies or saving fetched pages locally.")
#         file_path = f"{CACHE_LOCATION}/{franchise.name}_{season_number}.txt"
#         if os.path.exists(file_path):
#             with open(file_path, "r", encoding="utf-8") as f:
#                 wiki_text = f.read()
#                 print(f"Read wiki page from {file_path}")
    
#         else:
#             print(f"Fetching wiki page of {franchise.name} ({franchise.title}) season {season_number}")
#             wiki_text=get_content(franchise, season_number, "Episodes")
#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(wiki_text)
#                 print(f"Saved wiki page to {file_path}")
#     else:
#         print(f"Fetching wiki page of {franchise.name} ({franchise.title}) season {season_number}")
#         wiki_text = get_content(franchise, season_number, "Episodes")

    

#     return wiki_text


def _fetch_full_page(franchise: Franchise, season_number: int) -> str:
    """
    Fetch the ENTIRE raw wikitext for a season page in a single API call.

    Args:
        franchise:     The Franchise enum member.
        season_number: The season number.

    Returns:
        Raw wikitext for the full page.

    Raises:
        ValueError: If the page does not exist.
    """
    page_name = franchise.page_name.format(season_number)
    params = {
        "action": "parse",
        "page":   page_name,
        "prop":   "wikitext",     # no "section" param → returns the WHOLE page
        "format": "json",
    }

    response = polite_fetch_with_retry(CONSTANTS.WIKI_URL, params=params)
    time.sleep(SLEEP_DURATION)
    data = response.json()

    if "error" in data:
        raise ValueError(f"Wiki page not found: '{page_name}'")

    return data["parse"]["wikitext"]["*"]


def fetch_wiki_page(franchise: Franchise, season_number: int, use_cache: bool = True) -> str:
    """
    Fetch the full raw wikitext for a season, using local cache if available.

    Args:
        franchise:     The Franchise enum member.
        season_number: The season number.
        use_cache:     If True, reads/writes data/wiki_pages/{code}_S{nn}_raw.txt.

    Returns:
        Raw wikitext for the full page.
    """
    if not use_cache:
        print(f"Fetching {franchise.title} season {season_number} (no cache)...")
        return _fetch_full_page(franchise, season_number)

    CACHE_LOCATION.mkdir(parents=True, exist_ok=True)
    file_path = CACHE_LOCATION / f"{franchise.name}_S{season_number:02d}_raw.txt"

    if file_path.exists():
        print(f"Read cached wiki page from {file_path}")
        return file_path.read_text(encoding="utf-8")

    print(f"Fetching {franchise.title} season {season_number} from wiki...")
    wiki_text = _fetch_full_page(franchise, season_number)
    file_path.write_text(wiki_text, encoding="utf-8")
    print(f"Cached raw wiki page → {file_path}")

    return wiki_text
    