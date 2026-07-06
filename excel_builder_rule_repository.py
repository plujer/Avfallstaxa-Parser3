from __future__ import annotations

import argparse

from excel_builder.rules import MasterRuleRepositoryReader
from excel_builder.reports import RuleRepositoryReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Master Rule Repository from workbook")
    parser.add_argument("--workbook", default="data/ArbetsExcel_Reference.xlsx")
    parser.add_argument("--txt", default="output/excel/master_rule_repository_report.txt")
    parser.add_argument("--csv", default="output/excel/master_rule_repository.csv")
    args = parser.parse_args()

    repo = MasterRuleRepositoryReader().read(args.workbook)

    txt = RuleRepositoryReporter().write_txt(repo, args.txt)
    csv = RuleRepositoryReporter().write_csv(repo, args.csv)

    print("Master Rule Repository klar")
    print(f"Workbook: {args.workbook}")
    print(f"Rules: {repo.rule_count}")
    print(f"EDP rules: {len(repo.edp_rules)}")
    print(f"Taxepunkt rules: {len(repo.taxepunkt_rules)}")
    print(f"Documentation rules: {len(repo.documentation_rules)}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
