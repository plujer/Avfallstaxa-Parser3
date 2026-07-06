"""Write a report from the Excel Builder rulebook."""

from __future__ import annotations

from pathlib import Path
from collections import Counter

from excel_builder.models import Rulebook


class RulebookReporter:
    def write(self, rulebook: Rulebook, validation_warnings: list[str], path: str | Path = "output/excel/edp_rulebook_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        by_sheet = Counter(entry.source_sheet for entry in rulebook.entries)

        lines = [
            "Excel Builder EDP Rulebook Report",
            "",
            "Status: Read-only rule extraction from Arbets-Excel.",
            "Arbets-Excel is not master.",
            "",
            f"Rule entries: {rulebook.count}",
            f"Workbook warnings: {len(rulebook.warnings)}",
            f"Validation warnings: {len(validation_warnings)}",
            "",
            "Rule entries by sheet:",
        ]

        for sheet, count in sorted(by_sheet.items()):
            lines.append(f"- {sheet}: {count}")

        if rulebook.warnings:
            lines.append("")
            lines.append("Workbook warnings:")
            for warning in rulebook.warnings:
                lines.append(f"- {warning}")

        if validation_warnings:
            lines.append("")
            lines.append("Validation warnings:")
            for warning in validation_warnings:
                lines.append(f"- {warning}")

        lines.append("")
        lines.append("Key extracted rules:")
        for entry in rulebook.entries:
            text_norm = entry.text.lower()
            if any(token.lower() in text_norm for token in [
                "strtaxekod",
                "strtaxebenamning",
                "strtaxedelavser",
                "strfaktor",
                "strformel",
                "taxa_från_edp",
                "taxa_saknas",
                "aktuellt pris",
                "taxakod",
            ]):
                lines.append(f"- {entry.source_sheet} row {entry.row_number}: {entry.text}")

        lines.append("")
        lines.append("All entries:")
        for entry in rulebook.entries:
            lines.append(f"- {entry.source_sheet} row {entry.row_number}: {entry.text}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
