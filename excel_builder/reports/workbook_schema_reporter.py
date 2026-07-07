"""Reports for workbook schema scanning."""

from __future__ import annotations
import csv
from pathlib import Path
from excel_builder.models.workbook_schema_models import WorkbookSchema

class WorkbookSchemaReporter:
    SHEET_HEADERS = [
        "Sheet","State","Rows","Columns","Detected header row","Detected headers",
        "Tables","Formula count","Data validations","Merged ranges count",
        "Hidden columns","Hidden rows count","Freeze panes","Auto filter",
    ]
    HEADER_HEADERS = ["Sheet","Candidate row","Score","Non-empty count","Values"]

    def write_txt(self, schema: WorkbookSchema, path: str | Path = "output/excel/workbook_schema_report.txt") -> Path:
        out = Path(path); out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Workbook Schema Report", "",
            "Status: Läser masterarbetsbokens struktur. Inga ändringar görs.",
            f"Workbook: {schema.workbook_path}",
            f"Sheets: {schema.sheet_count}",
            f"Defined names: {len(schema.defined_names)}",
            f"Warnings: {len(schema.warnings)}", "", "Sheets:",
        ]
        for sheet in schema.sheets:
            lines += [
                "", f"## {sheet.name}",
                f"- State: {sheet.visible_state}",
                f"- Size: {sheet.max_row} rows x {sheet.max_column} columns",
                f"- Detected header row: {sheet.detected_header_row}",
                f"- Headers: {' | '.join([h for h in sheet.detected_headers if h][:30])}",
                f"- Tables: {', '.join(sheet.tables)}",
                f"- Formulas: {sheet.formula_count}",
                f"- Data validations: {sheet.data_validations}",
                f"- Merged ranges: {len(sheet.merged_ranges)}",
                f"- Hidden columns: {', '.join(sheet.hidden_columns)}",
                f"- Hidden rows: {len(sheet.hidden_rows)}",
            ]
            if sheet.header_candidates:
                lines.append("- Header candidates:")
                for candidate in sheet.header_candidates[:5]:
                    values = " | ".join([value for value in candidate.values if value][:20])
                    lines.append(f"  - row {candidate.row_number}, score {candidate.score}, non-empty {candidate.non_empty_count}: {values}")
        if schema.warnings:
            lines.append(""); lines.append("Warnings:")
            lines += [f"- {warning}" for warning in schema.warnings]
        out.write_text("\\n".join(lines), encoding="utf-8")
        return out

    def write_sheets_csv(self, schema: WorkbookSchema, path: str | Path = "output/excel/workbook_schema_sheets.csv") -> Path:
        out = Path(path); out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";"); writer.writerow(self.SHEET_HEADERS)
            for sheet in schema.sheets:
                writer.writerow([
                    sheet.name, sheet.visible_state, sheet.max_row, sheet.max_column,
                    sheet.detected_header_row or "", " | ".join([v for v in sheet.detected_headers if v]),
                    " | ".join(sheet.tables), sheet.formula_count, sheet.data_validations,
                    len(sheet.merged_ranges), " | ".join(sheet.hidden_columns), len(sheet.hidden_rows),
                    sheet.freeze_panes, sheet.auto_filter_ref,
                ])
        return out

    def write_headers_csv(self, schema: WorkbookSchema, path: str | Path = "output/excel/workbook_schema_header_candidates.csv") -> Path:
        out = Path(path); out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";"); writer.writerow(self.HEADER_HEADERS)
            for sheet in schema.sheets:
                for candidate in sheet.header_candidates:
                    writer.writerow([sheet.name, candidate.row_number, candidate.score, candidate.non_empty_count, " | ".join([v for v in candidate.values if v])])
        return out
