from constants import Franchise
import fetcher as fetcher
import extractor as extractor
import validation_report as validation_report
import os

CACHING_PAGES = True
CACHE_LOCATION = "./wiki_pages"

def run_etl(franchise: Franchise, season_number: int):
    """Full ETL pipeline for a single season."""

    # Step 1 — Fetch
    if CACHING_PAGES:
        print("Caching enabled")
        file_path = f"{CACHE_LOCATION}/{franchise.name}_{season_number}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                wiki_text = f.read()
                print(f"Read wiki_text from {file_path}")
    
        else:
            wiki_text = fetcher.fetch_wiki_page(franchise, season_number)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(wiki_text)
                print(f"Saved wiki_text to {file_path}")
    else:
        wiki_text = fetcher.fetch_wiki_page(franchise, season_number)


    # Step 2 — Extract
    season_model = extractor.extract_season_data(wiki_text, franchise, season_number)

    # Step 3 — Insert
    #report = ValidationReport(franchise=franchise.short_code, season_number=season_number)
    #insert_season(season_model, db_conn, report)

    # Step 4 — Write report
    #report.write()