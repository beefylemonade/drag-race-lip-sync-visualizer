import json
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
from constants import Franchise

class ReportEntry(BaseModel):
    field:   str
    context: dict
    reason:  str

class ValidationReport(BaseModel):
    franchise_short_code: str
    season_number:        int
    entries:              list[ReportEntry] = Field(default_factory=list)

    def log(self, field: str, context: dict, reason: str):
        """
        Log an ambiguous or missing field for manual review.

        Args:
            field:   The field name that requires review (e.g. 'lipsync.song').
            context: Dict identifying where the issue occurred
                     (e.g. {'episode': 3, 'lipsync_index': 1}).
            reason:  Description of the issue.
        """
        self.entries.append(ReportEntry(field=field, context=context, reason=reason))

    def write(self, output_dir: str = "reports"):
        """
        Write the validation report to a JSON file.

        Args:
            output_dir: Directory to write the report into.
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        filename = (
            f"{output_dir}/"
            f"{self.franchise_short_code}_S{self.season_number:02d}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        report = {
            "franchise": self.franchise_short_code,
            "season":    self.season_number,
            "generated": datetime.now().isoformat(),
            "issues":    [entry.model_dump() for entry in self.entries]
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Validation report written to {filename}")
        if self.entries:
            print(f"{len(self.entries)} issue(s) require manual review.")
        else:
            print(f"No issues found.")