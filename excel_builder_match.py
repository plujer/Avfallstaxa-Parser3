from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader, WorkbookTaxepunkterReader
from excel_builder.matching import MatchingEngine
from excel_builder.reports import MatchingReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Excel Builder Matching Engine preview")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--txt", default="output/excel/excel_matching_report.txt")
    parser.add_argument("--csv", default="output/excel/excel_matching_results.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    workbook_rows = WorkbookTaxepunkterReader().read(args.workbook)

    report = MatchingEngine().match(parser_rows, workbook_rows)

    txt = MatchingReporter().write_txt(report, args.txt)
    csv = MatchingReporter().write_csv(report, args.csv)

    print("Excel Builder Matching preview klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Workbook rows: {len(workbook_rows)}")
    print(f"EXACT: {report.exact}")
    print(f"PROBABLE: {report.probable}")
    print(f"REVIEW: {report.review}")
    print(f"NEW: {report.new}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
