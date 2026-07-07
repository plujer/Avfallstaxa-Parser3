from __future__ import annotations

import argparse

from excel_builder.builder import TaxepunkterRowBuilder
from excel_builder.io import ParserMatchReader, WorkbookTaxepunkterReader
from excel_builder.reports import RowBuilderReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Build complete Taxepunkter row plan")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--txt", default="output/excel/taxepunkter_row_plan_report.txt")
    parser.add_argument("--csv", default="output/excel/taxepunkter_row_plan.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    workbook_rows = WorkbookTaxepunkterReader().read(args.workbook)

    plan = TaxepunkterRowBuilder().build_plan(parser_rows, workbook_rows)

    txt = RowBuilderReporter().write_txt(plan, args.txt)
    csv = RowBuilderReporter().write_csv(plan, args.csv)

    print("Taxepunkter row plan klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Workbook rows: {len(workbook_rows)}")
    print(f"REUSE: {plan.reuse_count}")
    print(f"CREATE: {plan.create_count}")
    print(f"REVIEW: {plan.review_count}")
    print(f"Coverage plan valid: {plan.passed_coverage}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
