from __future__ import annotations

import argparse

from excel_builder.document import DocumentStructureEngine
from excel_builder.io import ParserMatchReader
from excel_builder.reports import DocumentStructureReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify parser rows into document structure row types")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--txt", default="output/excel/document_structure_report.txt")
    parser.add_argument("--csv", default="output/excel/document_structure_rows.csv")
    args = parser.parse_args()

    rows = ParserMatchReader().read(args.parser_result)
    report = DocumentStructureEngine().classify(rows)

    txt = DocumentStructureReporter().write_txt(report, args.txt)
    csv = DocumentStructureReporter().write_csv(report, args.csv)

    print("Document Structure Engine klar")
    print(f"Rows: {report.total}")
    print(f"TAX_NODE: {report.count('TAX_NODE')}")
    print(f"SUBSECTION: {report.count('SUBSECTION')}")
    print(f"SECTION: {report.count('SECTION')}")
    print(f"TABLE_HEADER: {report.count('TABLE_HEADER')}")
    print(f"NOTE: {report.count('NOTE')}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
