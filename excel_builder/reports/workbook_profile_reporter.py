"""Write a readable Arbets-Excel profile report."""

from __future__ import annotations

from pathlib import Path

from excel_builder.models import WorkbookProfile


class WorkbookProfileReporter:
    def write(self, profile: WorkbookProfile, path: str | Path = "output/excel/arbets_excel_profile_report.txt") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Arbets-Excel Profile Report",
            "",
            f"Workbook: {profile.path}",
            f"Sheets: {profile.sheet_count}",
            f"Warnings: {len(profile.warnings)}",
            "",
            "IMPORTANT:",
            "This is read-only analysis. Arbets-Excel is not master.",
            "",
        ]

        if profile.warnings:
            lines.append("Warnings:")
            for warning in profile.warnings:
                lines.append(f"- {warning}")
            lines.append("")

        for sheet in profile.sheets:
            lines.append("=" * 100)
            lines.append(f"Sheet: {sheet.name}")
            lines.append(f"State: {sheet.hidden_state}")
            lines.append(f"Rows: {sheet.max_row}")
            lines.append(f"Columns: {sheet.max_column}")
            lines.append(f"Frozen panes: {sheet.frozen_panes}")
            lines.append(f"Likely header row: {sheet.likely_header_row}")
            lines.append(f"Detected fields: {sheet.detected_fields}")
            lines.append(f"Merged ranges: {len(sheet.merged_ranges)}")
            if sheet.merged_ranges:
                for rng in sheet.merged_ranges[:20]:
                    lines.append(f"  - {rng}")
                if len(sheet.merged_ranges) > 20:
                    lines.append(f"  ... {len(sheet.merged_ranges) - 20} more")

            lines.append("")
            lines.append("Tables:")
            if sheet.tables:
                for table in sheet.tables:
                    lines.append(f"- {table.name}: {table.ref} columns={table.columns}")
            else:
                lines.append("- none")

            lines.append("")
            lines.append("Data validations:")
            if sheet.data_validations:
                for dv in sheet.data_validations[:30]:
                    lines.append(f"- type={dv.type} sqref={dv.sqref} formula1={dv.formula1}")
                if len(sheet.data_validations) > 30:
                    lines.append(f"- ... {len(sheet.data_validations) - 30} more")
            else:
                lines.append("- none")

            lines.append("")
            lines.append("Columns:")
            for col in sheet.columns:
                hidden = "hidden" if col.hidden else "visible"
                lines.append(
                    f"- {col.letter} ({col.index}) header='{col.header}' "
                    f"{hidden} width={col.width} non_empty={col.non_empty_count} formulas={col.formula_count}"
                )
            lines.append("")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
