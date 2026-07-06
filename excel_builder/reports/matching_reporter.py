"""Write matching report for Excel Builder."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import MatchReport


class MatchingReporter:
    HEADERS = [
        "Status",
        "Metod",
        "Score",
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

    def write_txt(self, report: MatchReport, path: str | Path = "output/excel/excel_matching_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Excel Builder Matching Report",
            "",
            "Status: Read-only matching preview. Arbets-Excel is not master.",
            f"Total parser rows: {report.total}",
            f"EXACT: {report.exact}",
            f"PROBABLE: {report.probable}",
            f"REVIEW: {report.review}",
            f"NEW: {report.new}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Details:",
        ]

        for item in report.candidates:
            wb = item.workbook_row
            lines.append(
                f"- {item.status} score={item.score:.3f} method={item.method} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | "
                f"excel_row={wb.row_number if wb else ''} tax_code={wb.tax_code if wb else ''} | {item.comment}"
            )

        if report.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in report.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: MatchReport, path: str | Path = "output/excel/excel_matching_results.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for item in report.candidates:
                wb = item.workbook_row
                writer.writerow([
                    item.status,
                    item.method,
                    f"{item.score:.3f}",
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
