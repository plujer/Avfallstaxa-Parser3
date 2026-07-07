"""CLI for Semantic Attribute Intelligence."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.reports.semantic_attribute_reporter import SemanticAttributeReporter
from excel_builder.rules.master_rule_repository_reader import MasterRuleRepositoryReader
from excel_builder.semantic_attributes import SemanticAttributeRepository
from excel_builder.standard.standard_tax_reader import StandardTaxReader


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Semantic Attribute Intelligence reports.")
    parser.add_argument("--standard-tax", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    args = parser.parse_args()

    catalog = StandardTaxReader().read(Path(args.standard_tax))
    repo = MasterRuleRepositoryReader().read(Path(args.workbook))
    report = SemanticAttributeRepository().from_standard_and_rules(catalog, repo)
    SemanticAttributeReporter().write(report, args.out_dir)

    print("Semantic Attribute Intelligence klar.")
    print(f"Profiles: {report.total_profiles}")
    print(f"Profiles with attributes: {report.profiles_with_attributes}")
    print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
