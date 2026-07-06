"""Write Excel Builder text report."""

from __future__ import annotations

from pathlib import Path
from collections import Counter

from excel_builder.models import BuilderResult


class BuilderReporter:
    def write(self, result: BuilderResult, path: str | Path = "output/excel/excel_builder_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        sections = Counter(row.section for row in result.rows)

        lines = [
            "Excel Builder Report",
            "",
            "Status: Arbets-Excel, inte master",
            f"Rows read from parser: {result.row_count}",
            f"Warnings: {len(result.warnings)}",
            "",
            "Rows by section:",
        ]

        for section, count in sorted(sections.items()):
            lines.append(f"- {section}: {count}")

        if result.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in result.warnings:
                lines.append(f"- {warning}")

        out.write_text("\\n".join(lines), encoding="utf-8")
        return out
