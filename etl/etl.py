from constants import Franchise
from etl.fetcher import fetch_wiki_page
from etl.extractor import extract_season_data
#from etl.validation_report import 


use_cache = True


def run_etl(franchise: Franchise, season_number: int):
    """Full ETL pipeline for a single season."""

    # Step 1 — Fetch from local copy or from the wiki page
    
    wiki_text = fetch_wiki_page(franchise, season_number, use_cache = use_cache)


    # Step 2 — Extract
    season_model = extract_season_data(wiki_text, franchise, season_number)

    # Step 3 — Insert
    #report = ValidationReport(franchise=franchise.short_code, season_number=season_number)
    #insert_season(season_model, db_conn, report)

    # Step 4 — Write report
    #report.write()