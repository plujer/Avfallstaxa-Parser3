"""Write Workbook Generation Engine text reports."""

from __future__ import annotations

from pathlib import Path

from excel_builder.models import WorkbookGenerationReport


class WorkbookGenerationReporter:
    def write(self, report: WorkbookGenerationReport, out_dir: str | Path = "output/excel") -> None:
        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        lines = [
            "Workbook Generation Engine Report",
            "",
            "Status: Skriver beslutsspårning till Arbets-Excel utan att ändra Taxa_från_edp.",
            "Taxa_från_edp är facit. Standardtaxor och beslutsspår är endast beslutsstöd.",
            f"Workbook: {report.workbook_path}",
            f"Decision_Trace rows written: {report.rows_written}",
            f"Taxepunkter rows updated: {report.taxepunkter_rows_updated}",
            f"Warnings: {len(report.warnings)}",
        ]
        if report.warnings:
            lines += ["", "Warnings:"] + [f"- {warning}" for warning in report.warnings]
        (out_path / "workbook_generation_report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
