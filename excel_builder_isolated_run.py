from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.edp import EdpExportReader, IsolatedWorkbookBuilder
from excel_builder.reports import EdpRunReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Create isolated workbook for one EDP export")
    parser.add_argument("--municipality", required=True)
    parser.add_argument("--edp-export", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    args = parser.parse_args()

    municipality = args.municipality.strip()
    safe_name = municipality.replace("å", "a").replace("ä", "a").replace("ö", "o").replace("Å", "A").replace("Ä", "A").replace("Ö", "O").replace(" ", "_")

    out_dir = Path(args.out_dir) / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)

    export = EdpExportReader().read(args.edp_export, municipality=municipality)
    workbook_path = out_dir / f"ArbetsExcel_{safe_name}_byggd.xlsx"
    report_path = out_dir / f"edp_isolated_run_report_{safe_name}.txt"

    IsolatedWorkbookBuilder().build(export, workbook_path)
    EdpRunReporter().write(export, workbook_path, report_path)

    print("Isolerad EDP-körning klar")
    print(f"Kommun: {municipality}")
    print(f"EDP-export: {args.edp_export}")
    print(f"Rader: {export.row_count}")
    print(f"Excel: {workbook_path}")
    print(f"Rapport: {report_path}")


if __name__ == "__main__":
    main()
