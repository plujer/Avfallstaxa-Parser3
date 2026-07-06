from __future__ import annotations

import argparse

from excel_builder.io import ParserResultReader, WorkbookWriter
from excel_builder.reports import BuilderReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Excel Builder v2.0.0-alpha.1")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--out", default="output/excel/ArbetsExcel_byggd_fran_parser.xlsx")
    args = parser.parse_args()

    result = ParserResultReader().read(args.parser_result)
    workbook_path = WorkbookWriter().write(result, args.out)
    report_path = BuilderReporter().write(result)

    print("Excel Builder klar")
    print(f"Rader: {result.row_count}")
    print(f"Excel: {workbook_path}")
    print(f"Rapport: {report_path}")


if __name__ == "__main__":
    main()
