"""Write Word tax coverage reports."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import CoverageReport


class CoverageReporter:
    HEADERS = [
        "Status",
        "Metod",
        "Parser paragraf",
        "Parser taxapunkt",
        "Parser variant",
        "Parser enhet",
        "Excel rad",
        "Excel taxapunkt",
        "Excel variant",
        "Excel enhet",
        "Excel taxakod",
        "Kommentar",
    ]

    def write_txt(self, report: CoverageReport, path: str | Path = "output/excel/word_tax_coverage_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Word Tax Coverage Report",
            "",
            "KRAV:",
            "Alla taxor som hittas i Word måste finnas som egen rad i Taxepunkter.",
            "Detta gäller oavsett om Taxa_från_edp är tom eller saknar matchning.",
            "",
            f"Total parser rows: {report.total}",
            f"COVERED: {report.covered}",
            f"REVIEW: {report.review}",
            f"MISSING: {report.missing}",
            f"Passed: {report.passed}",
            "",
            "Details:",
        ]

        for item in report.items:
            wb = item.workbook_row
            lines.append(
                f"- {item.status} | {item.method} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | "
                f"excel_row={wb.row_number if wb else ''} tax_code={wb.tax_code if wb else ''} | "
                f"{item.comment}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: CoverageReport, path: str | Path = "output/excel/word_tax_coverage_results.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for item in report.items:
                wb = item.workbook_row
                writer.writerow([
                    item.status,
                    item.method,
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    wb.row_number if wb else "",
                    wb.tax_point if wb else "",
                    wb.variant if wb else "",
                    wb.unit if wb else "",
                    wb.tax_code if wb else "",
                    item.comment,
                ])

        return out
