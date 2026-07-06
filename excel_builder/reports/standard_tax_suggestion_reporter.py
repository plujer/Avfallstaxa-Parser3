"""Reports for standard tax suggestions."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import StandardTaxSuggestionReport


class StandardTaxSuggestionReporter:
    HEADERS = [
        "Status",
        "Score",
        "Metod",
        "Parser paragraf",
        "Parser taxapunkt",
        "Parser variant",
        "Parser enhet",
        "Föreslagen strTaxekod",
        "Föreslagen strTaxebenamning",
        "Föreslagen strFaktor",
        "Föreslagen strTaxedelAvser",
        "Föreslagen strFormel",
        "Källa",
        "Kommentar",
    ]

    def write_txt(self, report: StandardTaxSuggestionReport, path: str | Path = "output/excel/standard_tax_suggestions_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Standard Tax Suggestions Report",
            "",
            "Status: Förslag från standardtaxor. Ej bekräftad kommun-EDP.",
            f"Total parser rows: {report.total}",
            f"PROPOSAL: {report.proposal_count}",
            f"REVIEW: {report.review_count}",
            f"NO_SUGGESTION: {report.no_suggestion_count}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Details:",
        ]

        for item in report.suggestions:
            standard = item.standard_row
            lines.append(
                f"- {item.status} score={item.score:.3f} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | "
                f"suggested={standard.strTaxekod if standard else ''} "
                f"{standard.strTaxebenamning if standard else ''} | {item.comment}"
            )

        if report.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in report.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: StandardTaxSuggestionReport, path: str | Path = "output/excel/standard_tax_suggestions.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for item in report.suggestions:
                standard = item.standard_row
                writer.writerow([
                    item.status,
                    f"{item.score:.3f}",
                    item.method,
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    standard.strTaxekod if standard else "",
                    standard.strTaxebenamning if standard else "",
                    standard.strFaktor if standard else "",
                    standard.strTaxedelAvser if standard else "",
                    standard.strFormel if standard else "",
                    f"{standard.source_sheet} row {standard.row_number}" if standard else "",
                    item.comment,
                ])

        return out
