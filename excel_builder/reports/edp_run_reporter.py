"""Report for isolated EDP export runs."""

from __future__ import annotations

from pathlib import Path

from excel_builder.models import EdpExport


class EdpRunReporter:
    def write(self, export: EdpExport, workbook_path: str | Path, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Excel Builder Isolated EDP Run Report",
            "",
            f"Kommun: {export.municipality}",
            f"EDP-källa: {export.source_path}",
            f"EDP-rader: {export.row_count}",
            f"Output workbook: {workbook_path}",
            f"Warnings: {len(export.warnings)}",
            "",
            "KRAV:",
            "Varje EDP-export ska skapa ett unikt Excel-dokument.",
            "EDP-data får inte blandas mellan kommuner eller användas i fel Excel/Word-fil.",
            "Generella regelverk får återanvändas mellan dokument.",
        ]

        if export.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in export.warnings:
                lines.append(f"- {warning}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
