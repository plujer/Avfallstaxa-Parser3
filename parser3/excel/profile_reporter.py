"""Write workbook profile report."""

from __future__ import annotations

from pathlib import Path
from parser3.excel.excel_models import WorkbookProfile


class ProfileReporter:
    def write(self, profile: WorkbookProfile, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Parser 3.1 Master.xlsx profile report",
            "",
            f"Workbook: {profile.path}",
            "",
        ]

        best = profile.best_sheet
        if best:
            lines.append(f"Best sheet: {best.sheet_name}")
            lines.append(f"Best score: {best.candidate_score}")
            lines.append("")

        for sheet in profile.sheets:
            lines.append(f"Sheet: {sheet.sheet_name}")
            lines.append(f"  rows: {sheet.max_row}")
            lines.append(f"  columns: {sheet.max_column}")
            lines.append(f"  header_row: {sheet.header_row}")
            lines.append(f"  score: {sheet.candidate_score}")
            lines.append(f"  detected_columns: {sheet.detected_columns}")
            if sheet.headers:
                lines.append("  headers:")
                for idx, header in enumerate(sheet.headers, start=1):
                    if header:
                        lines.append(f"    {idx}: {header}")
            lines.append("")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
