from __future__ import annotations

import argparse

from excel_builder.edp import EdpExportReader
from excel_builder.standard import StandardTaxReader, EdpStandardDeviationEngine, DeviationWorkbookWriter


def main() -> None:
    parser = argparse.ArgumentParser(description="Write EDP standard deviation analysis to workbook")
    parser.add_argument("--municipality", required=True)
    parser.add_argument("--edp-export", required=True)
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", required=True)
    args = parser.parse_args()

    edp_export = EdpExportReader().read(args.edp_export, args.municipality)
    catalog = StandardTaxReader().read(args.standard_tax)
    report = EdpStandardDeviationEngine().compare(edp_export, catalog)
    DeviationWorkbookWriter().write(args.workbook, report)

    print("EDP standardavvikelser skrivna till arbetsbok")
    print(f"Kommun: {args.municipality}")
    print(f"EDP rows: {edp_export.row_count}")
    print(f"Standard rows: {catalog.row_count}")
    print(f"REVIEW: {report.review_count}")
    print(f"OK: {report.ok_count}")
    print(f"Workbook: {args.workbook}")


if __name__ == "__main__":
    main()
