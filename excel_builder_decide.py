from __future__ import annotations

import argparse

from excel_builder.decision import DecisionWorkbookWriter, TaxDecisionEngine
from excel_builder.io import ParserMatchReader, WorkbookTaxepunkterReader
from excel_builder.standard import StandardTaxReader, StandardTaxSuggestionEngine
from excel_builder.reports import DecisionReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Create consolidated tax decisions")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--reference-workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--municipality", default="")
    parser.add_argument("--txt", default="output/excel/tax_decision_report.txt")
    parser.add_argument("--csv", default="output/excel/tax_decision_results.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    workbook_rows = WorkbookTaxepunkterReader().read(args.reference_workbook)
    catalog = StandardTaxReader().read(args.standard_tax)
    suggestions = StandardTaxSuggestionEngine().suggest(parser_rows, catalog)

    report = TaxDecisionEngine().decide(parser_rows, workbook_rows, suggestions)

    DecisionReporter().write_txt(report, args.txt)
    DecisionReporter().write_csv(report, args.csv)
    DecisionWorkbookWriter().write(args.workbook, report, municipality=args.municipality)

    print("Tax Decision Engine klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Workbook rows: {len(workbook_rows)}")
    print(f"EDP_MATCH: {report.edp_match}")
    print(f"STANDARD_PROPOSAL: {report.standard_proposal}")
    print(f"REVIEW_REQUIRED: {report.review_required}")
    print(f"NEW_TAXA: {report.new_taxa}")
    print(f"Workbook: {args.workbook}")


if __name__ == "__main__":
    main()
