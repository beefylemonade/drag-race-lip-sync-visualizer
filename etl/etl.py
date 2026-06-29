from constants import Franchise
import fetcher as fetcher
import extractor as extractor
import validation_report as validation_report


use_cache = True


def run_etl(franchise: Franchise, season_number: int):
    """Full ETL pipeline for a single season."""

    # Step 1 — Fetch from local copy or from the wiki page
    
    wiki_text = fetcher.fetch_wiki_page(franchise, season_number, use_cache = use_cache)


    # Step 2 — Extract
    season_model = extractor.extract_season_data(wiki_text, franchise, season_number)

    # Step 3 — Insert
    #report = ValidationReport(franchise=franchise.short_code, season_number=season_number)
    #insert_season(season_model, db_conn, report)

    # Step 4 — Write report
    #report.write()