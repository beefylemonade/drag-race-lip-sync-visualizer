from constants import Franchise
from etl.fetcher import fetch_wiki_page
from etl.extractor import extract_data
from etl.caching import save_extracted_data, load_extracted_data
from etl.validation_report import ValidationReport


use_cache = True
report_path = './reports'


def run_etl(franchise: Franchise, season_number: int):
    """Full ETL pipeline for a single season."""

    season = load_extracted_data(franchise, season_number)

    print(f"Starting ETL for {franchise.title} Season {season_number}...")

    # ── Step 1: Load local file if it exists, otherwise fetch + extract ──

    season = load_extracted_data(franchise, season_number)

    if season is None:
        # Step 1 — Fetch from local copy or from the wiki page
        print(f"  Fetching wiki page...")
        wiki_text = fetch_wiki_page(franchise, season_number, use_cache = use_cache)

        print(f"  Extracting via LLM...")
        # Step 2 — Extract (and save a local copy)
        season = extract_data(wiki_text, franchise, season_number, use_cache = use_cache)

    else:
        print(f"  Skipping LLM extraction — using local file.")


    # Step 3 — Insert
    #report = ValidationReport(franchise_short_code=franchise.name, season_number=season_number)
    #insert_season(season_model, db_conn, report)

    # Step 4 — Write report
    #report.write(report_path)