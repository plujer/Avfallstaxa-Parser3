from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader, WorkbookTaxepunkterReader
from excel_builder.reports import CoverageReporter
from excel_builder.validation import WordTaxCoverageValidator


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Word tax coverage in Taxepunkter")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--workbook", default="output/excel/ArbetsExcel_byggd_fran_parser.xlsx")
    parser.add_argument("--txt", default="output/excel/word_tax_coverage_report.txt")
    parser.add_argument("--csv", default="output/excel/word_tax_coverage_results.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    workbook_rows = WorkbookTaxepunkterReader().read(args.workbook)

    report = WordTaxCoverageValidator().validate(parser_rows, workbook_rows)

    txt = CoverageReporter().write_txt(report, args.txt)
    csv = CoverageReporter().write_csv(report, args.csv)

    print("Word Tax Coverage klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Workbook rows: {len(workbook_rows)}")
    print(f"COVERED: {report.covered}")
    print(f"REVIEW: {report.review}")
    print(f"MISSING: {report.missing}")
    print(f"Passed: {report.passed}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
