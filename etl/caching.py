from pathlib import Path
from models import SeasonModel
from constants import Franchise

DATA_DIR = Path("data/extracted")

def save_extracted_data(season: SeasonModel, franchise: Franchise, season_number: int) -> Path:
    """
    Save a validated SeasonModel to a local JSON file.

    Args:
        season:        The validated SeasonModel to persist.
        franchise:     The Franchise enum member.
        season_number: The season number.

    Returns:
        Path to the saved file.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"{franchise.short_code}_S{season_number:02d}.json"
    path.write_text(season.model_dump_json(indent=2))
    print(f"  Extracted data saved → {path}")
    return path


def load_extracted_data(franchise: Franchise, season_number: int) -> SeasonModel | None:
    """
    Load a previously saved SeasonModel from a local JSON file.

    Args:
        franchise:     The Franchise enum member.
        season_number: The season number.

    Returns:
        SeasonModel if a local file exists, None otherwise.
    """
    path = DATA_DIR / f"{franchise.short_code}_S{season_number:02d}.json"
    if not path.exists():
        return None
    print(f"  Found local extracted data → {path}")
    return SeasonModel.model_validate_json(path.read_text())