from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.standard import StandardTaxReader, StandardTaxSuggestionEngine
from excel_builder.reports import StandardTaxSuggestionReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Suggest missing tax codes from standard tax catalog")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--txt", default="output/excel/standard_tax_suggestions_report.txt")
    parser.add_argument("--csv", default="output/excel/standard_tax_suggestions.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    catalog = StandardTaxReader().read(args.standard_tax)
    report = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    txt = StandardTaxSuggestionReporter().write_txt(report, args.txt)
    csv = StandardTaxSuggestionReporter().write_csv(report, args.csv)

    print("Standard Tax Suggestions klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Standard rows: {catalog.row_count}")
    print(f"PROPOSAL: {report.proposal_count}")
    print(f"REVIEW: {report.review_count}")
    print(f"NO_SUGGESTION: {report.no_suggestion_count}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
