from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.knowledge import TaxKnowledgeExtractor, KnowledgeWorkbookWriter
from excel_builder.reports import KnowledgeReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract tax knowledge features from parser rows")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--txt", default="output/excel/tax_knowledge_report.txt")
    parser.add_argument("--csv", default="output/excel/tax_knowledge_features.csv")
    parser.add_argument("--workbook", default="")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    report = TaxKnowledgeExtractor().extract(parser_rows)

    txt = KnowledgeReporter().write_txt(report, args.txt)
    csv = KnowledgeReporter().write_csv(report, args.csv)

    if args.workbook:
        KnowledgeWorkbookWriter().write(args.workbook, report)

    print("Tax Knowledge extraction klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Features: {report.total}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")
    if args.workbook:
        print(f"Workbook updated: {args.workbook}")


if __name__ == "__main__":
    main()
