"""Reports for parser context resolution."""

from __future__ import annotations

import csv
from pathlib import Path

from excel_builder.models import ContextResolutionReport


class ContextResolutionReporter:
    HEADERS = [
        "Index",
        "Section",
        "Original tax point",
        "Enriched tax point",
        "Section context",
        "Property context",
        "Waste context",
        "Service context",
        "Container context",
        "Confidence",
        "Notes",
    ]

    def write_txt(self, report: ContextResolutionReport, path: str | Path = "output/excel/context_resolution_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Context Resolution Report",
            "",
            "Status: Berikar parserrader med kontext från sektion/rubriker/närliggande rader.",
            "Detta ändrar inte originalparsern och inte Taxa_från_edp.",
            f"Rows: {report.total}",
            f"Enriched rows: {report.enriched_count}",
            f"Warnings: {len(report.warnings)}",
            "",
            "Examples:",
        ]

        for row in report.rows[:80]:
            if row.enriched_row != row.original_row:
                lines.append(
                    f"- {row.context.row_index}: {row.original_row.tax_point} -> {row.enriched_row.tax_point} "
                    f"| context={row.context.inherited_text}"
                )

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def write_csv(self, report: ContextResolutionReport, path: str | Path = "output/excel/context_resolved_rows.csv") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADERS)
            for item in report.rows:
                ctx = item.context
                writer.writerow([
                    ctx.row_index,
                    item.original_row.section,
                    item.original_row.tax_point,
                    item.enriched_row.tax_point,
                    ctx.section_context,
                    ctx.property_type_context,
                    ctx.waste_type_context,
                    ctx.service_context,
                    ctx.container_context,
                    f"{ctx.confidence:.2f}",
                    " | ".join(ctx.notes),
                ])

        return out
