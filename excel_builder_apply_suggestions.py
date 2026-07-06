from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.standard import StandardTaxReader, StandardTaxSuggestionEngine, SuggestionWorkbookWriter
from excel_builder.reports import StandardTaxSuggestionReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Write standard tax suggestions into workbook")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--municipality", default="")
    parser.add_argument("--txt", default="output/excel/standard_tax_suggestions_report.txt")
    parser.add_argument("--csv", default="output/excel/standard_tax_suggestions.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    catalog = StandardTaxReader().read(args.standard_tax)
    report = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    StandardTaxSuggestionReporter().write_txt(report, args.txt)
    StandardTaxSuggestionReporter().write_csv(report, args.csv)
    SuggestionWorkbookWriter().write(args.workbook, report, municipality=args.municipality)

    print("Standardtaxeförslag skrivna till arbetsbok")
    print(f"Workbook: {args.workbook}")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Standard rows: {catalog.row_count}")
    print(f"PROPOSAL: {report.proposal_count}")
    print(f"REVIEW: {report.review_count}")
    print(f"NO_SUGGESTION: {report.no_suggestion_count}")


if __name__ == "__main__":
    main()
