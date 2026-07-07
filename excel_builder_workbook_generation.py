"""CLI for Workbook Generation Engine."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.workbook_generation import DecisionTraceCsvReader, WorkbookGenerationEngine
from excel_builder.reports.workbook_generation_reporter import WorkbookGenerationReporter


def main() -> int:
    parser = argparse.ArgumentParser(description="Write decision trace and review columns to Arbets-Excel.")
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--decision-traces", default="output/excel/decision_traces.csv")
    parser.add_argument("--out-dir", default="output/excel")
    args = parser.parse_args()

    rows = DecisionTraceCsvReader().read(Path(args.decision_traces))
    report = WorkbookGenerationEngine().write(Path(args.workbook), rows)
    WorkbookGenerationReporter().write(report, args.out_dir)

    print("Workbook Generation Engine klar.")
    print(f"Workbook: {report.workbook_path}")
    print(f"Decision_Trace rows: {report.rows_written}")
    print(f"Taxepunkter updated: {report.taxepunkter_rows_updated}")
    print(f"Warnings: {len(report.warnings)}")
    return 0 if report.status in {"OK", "WARNING"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
