"""Reports for standard catalog schema reverse engineering."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import StandardCatalogSchema


class StandardCatalogSchemaReporter:
    HEADERS = [
        "Sheet",
        "Rows",
        "Columns",
        "Section header row",
        "Start row",
        "End row",
        "Row count",
        "Key columns",
        "Headers",
        "Tables",
        "Formula count",
        "Merged ranges count",
    ]

    def write_txt(self, schema: StandardCatalogSchema, path: str | Path = "output/excel/standard_catalog_schema_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Standard Catalog Schema Report",
            "",
            "Status: Reverse engineering av standardtaxefilen.",
            "Originalfilen ändras inte.",
            f"Source: {schema.source_path}",
            f"Sheets: {schema.sheet_count}",
            f"Sections: {schema.section_count}",
            f"Estimated standard rows: {schema.estimated_standard_rows}",
            f"Warnings: {len(schema.warnings)}",
            "",
            "Sheets:",
        ]

        for sheet in schema.sheets:
            lines.append("")
            lines.append(f"## {sheet.name}")
            lines.append(f"- Size: {sheet.max_row} rows x {sheet.max_column} columns")
            lines.append(f"- Sections: {len(sheet.sections)}")
            lines.append(f"- Tables: {', '.join(sheet.tables)}")
            lines.append(f"- Formulas: {sheet.formula_count}")
            lines.append(f"- Merged ranges: {len(sheet.merged_ranges)}")
            for section in sheet.sections:
                lines.append(
                    f"  - header row {section.header_row}, rows {section.start_row}-{section.end_row}, "
                    f"count {section.row_count}, key columns: {', '.join(section.key_columns)}"
                )

        if schema.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in schema.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, schema: StandardCatalogSchema, path: str | Path = "output/excel/standard_catalog_schema.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)

            for sheet in schema.sheets:
                if not sheet.sections:
                    writer.writerow([
                        sheet.name,
                        sheet.max_row,
                        sheet.max_column,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        " | ".join(sheet.tables),
                        sheet.formula_count,
                        len(sheet.merged_ranges),
                    ])

                for section in sheet.sections:
                    writer.writerow([
                        sheet.name,
                        sheet.max_row,
                        sheet.max_column,
                        section.header_row,
                        section.start_row,
                        section.end_row,
                        section.row_count,
                        " | ".join(section.key_columns),
                        " | ".join([header for header in section.headers if header]),
                        " | ".join(sheet.tables),
                        sheet.formula_count,
                        len(sheet.merged_ranges),
                    ])

        return out
