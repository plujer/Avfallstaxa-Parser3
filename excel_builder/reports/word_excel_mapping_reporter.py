"""Report writer for Word to Excel mapping."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models.word_excel_mapping_models import WordExcelMappingReport


class WordExcelMappingReporter:
    HEADERS = [
        "WordTaxID",
        "Status",
        "Metod",
        "Confidence",
        "Word paragraf",
        "Word taxapunkt",
        "Word variant",
        "Word enhet",
        "Excel rad",
        "Excel paragraf",
        "Excel taxapunkt",
        "Excel variant",
        "Excel enhet",
        "Excel taxakod",
        "Duplicate EDP allowed",
        "Kommentar",
    ]

    def write_txt(self, report: WordExcelMappingReport, path: str | Path = "output/excel/word_excel_mapping_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Word Excel Mapping Report",
            "",
            "Syfte:",
            "Skapar spårbar mappning mellan varje Word/parser-taxa och motsvarande rad i Taxepunkter.",
            "",
            "Regler:",
            "- Word-master ändras aldrig.",
            "- Excel-master ändras aldrig.",
            "- Taxepunkter A:E ändras aldrig automatiskt.",
            "- Taxa_från_edp ändras aldrig.",
            "- Samma EDP-taxa kan användas av flera Word-rader utan att det automatiskt är fel.",
            "",
            f"Total Word rows: {report.total}",
            f"MAPPED: {report.mapped}",
            f"REVIEW: {report.review}",
            f"MISSING: {report.missing}",
            f"Passed: {report.passed}",
            "",
            "Details:",
        ]
        for item in report.items:
            wb = item.workbook_row
            lines.append(
                f"- {item.word_tax_id} | {item.status} | {item.method} | "
                f"{item.parser_row.section} | {item.parser_row.tax_point} | "
                f"excel_row={wb.row_number if wb else ''} tax_code={wb.tax_code if wb else ''} | {item.comment}"
            )
        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: WordExcelMappingReport, path: str | Path = "output/excel/word_excel_mapping.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for item in report.items:
                wb = item.workbook_row
                writer.writerow([
                    item.word_tax_id,
                    item.status,
                    item.method,
                    item.confidence,
                    item.parser_row.section,
                    item.parser_row.tax_point,
                    item.parser_row.variant,
                    item.parser_row.unit,
                    wb.row_number if wb else "",
                    wb.section if wb else "",
                    wb.tax_point if wb else "",
                    wb.variant if wb else "",
                    wb.unit if wb else "",
                    wb.tax_code if wb else "",
                    "YES" if item.duplicate_edp_allowed else "NO",
                    item.comment,
                ])
        return out
