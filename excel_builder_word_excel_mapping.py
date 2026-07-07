from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader, WorkbookTaxepunkterReader
from excel_builder.reports.word_excel_mapping_reporter import WordExcelMappingReporter
from excel_builder.word_excel_mapping import WordExcelMappingEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Build deterministic Word to Excel mapping report")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--workbook", default="output/excel/ArbetsExcel_byggd_fran_parser.xlsx")
    parser.add_argument("--txt", default="output/excel/word_excel_mapping_report.txt")
    parser.add_argument("--csv", default="output/excel/word_excel_mapping.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    workbook_rows = WorkbookTaxepunkterReader().read(args.workbook)
    report = WordExcelMappingEngine().build(parser_rows, workbook_rows)

    txt = WordExcelMappingReporter().write_txt(report, args.txt)
    csv = WordExcelMappingReporter().write_csv(report, args.csv)

    print("Word Excel Mapping klar")
    print(f"Word rows: {len(parser_rows)}")
    print(f"Workbook rows: {len(workbook_rows)}")
    print(f"MAPPED: {report.mapped}")
    print(f"REVIEW: {report.review}")
    print(f"MISSING: {report.missing}")
    print(f"Passed: {report.passed}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
