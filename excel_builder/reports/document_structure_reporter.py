"""Reports for Document Structure Engine."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models.document_structure_models import DocumentRowType, DocumentStructureReport


class DocumentStructureReporter:
    HEADERS = [
        "Index",
        "Row type",
        "Section",
        "Tax point",
        "Variant",
        "Unit",
        "Price",
        "Parent index",
        "Level",
        "Confidence",
        "Reason",
    ]

    def write_txt(self, report: DocumentStructureReport, path: str | Path = "output/excel/document_structure_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Document Structure Engine Report",
            "",
            "Status: Klassificerar parserrader innan semantik och beslut.",
            "Taxa_från_edp ändras inte. Originalparserrader bevaras.",
            f"Rows: {report.total}",
        ]
        for row_type in DocumentRowType:
            lines.append(f"{row_type.value}: {report.count(row_type)}")
        lines.extend([
            f"Warnings: {len(report.warnings)}",
            "",
            "Non-tax structure examples:",
        ])

        examples = [node for node in report.nodes if node.row_type != DocumentRowType.TAX_NODE][:80]
        for node in examples:
            lines.append(
                f"- {node.row_index}: {node.row_type.value} | {node.parser_row.section} | "
                f"{node.parser_row.tax_point} | {node.reason}"
            )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: DocumentStructureReport, path: str | Path = "output/excel/document_structure_rows.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for node in report.nodes:
                row = node.parser_row
                writer.writerow([
                    node.row_index,
                    node.row_type.value,
                    row.section,
                    row.tax_point,
                    row.variant,
                    row.unit,
                    row.price,
                    node.parent_index or "",
                    node.level,
                    f"{node.confidence:.2f}",
                    node.reason,
                ])

        return out
