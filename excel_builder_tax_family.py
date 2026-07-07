"""CLI for Tax Family Intelligence."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.rules.master_rule_repository_reader import MasterRuleRepositoryReader
from excel_builder.reports.tax_family_reporter import TaxFamilyReporter
from excel_builder.standard.standard_tax_reader import StandardTaxReader
from excel_builder.tax_family import TaxFamilyRepository


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Tax Family Intelligence reports.")
    parser.add_argument("--standard-tax", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    args = parser.parse_args()

    catalog = StandardTaxReader().read(Path(args.standard_tax))
    repo = MasterRuleRepositoryReader().read(Path(args.workbook))
    report = TaxFamilyRepository().from_standard_and_rules(catalog, repo)
    TaxFamilyReporter().write(report, args.out_dir)

    print("Tax Family Intelligence klar.")
    print(f"Families: {report.total_families}")
    print(f"Members: {report.total_members}")
    print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
