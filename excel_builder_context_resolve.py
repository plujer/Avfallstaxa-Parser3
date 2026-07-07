from __future__ import annotations

import argparse

from excel_builder.context import ParserContextResolver
from excel_builder.io import ParserMatchReader
from excel_builder.reports import ContextResolutionReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve parser row context")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--txt", default="output/excel/context_resolution_report.txt")
    parser.add_argument("--csv", default="output/excel/context_resolved_rows.csv")
    args = parser.parse_args()

    rows = ParserMatchReader().read(args.parser_result)
    report = ParserContextResolver().resolve(rows)

    txt = ContextResolutionReporter().write_txt(report, args.txt)
    csv = ContextResolutionReporter().write_csv(report, args.csv)

    print("Context Resolver klar")
    print(f"Rows: {report.total}")
    print(f"Enriched rows: {report.enriched_count}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
