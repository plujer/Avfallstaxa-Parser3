from __future__ import annotations

import argparse

from excel_builder.rules import RulebookReader, EdpRuleValidator
from excel_builder.reports import RulebookReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Read Excel Builder rulebook from Arbets-Excel")
    parser.add_argument("--workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--out", default="output/excel/edp_rulebook_report.txt")
    args = parser.parse_args()

    rulebook = RulebookReader().read(args.workbook)
    validation_warnings = EdpRuleValidator().validate(rulebook)
    report = RulebookReporter().write(rulebook, validation_warnings, args.out)

    print("EDP rulebook läst")
    print(f"Entries: {rulebook.count}")
    print(f"Workbook warnings: {len(rulebook.warnings)}")
    print(f"Validation warnings: {len(validation_warnings)}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
