"""CLI for Variant Intelligence Engine."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.reports.variant_intelligence_reporter import VariantIntelligenceReporter
from excel_builder.rules.master_rule_repository_reader import MasterRuleRepositoryReader
from excel_builder.standard.standard_tax_reader import StandardTaxReader
from excel_builder.variant_intelligence import VariantRepository


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Variant Intelligence reports.")
    parser.add_argument("--standard-tax", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    args = parser.parse_args()

    catalog = StandardTaxReader().read(Path(args.standard_tax))
    repo = MasterRuleRepositoryReader().read(Path(args.workbook))
    report = VariantRepository().from_standard_and_rules(catalog, repo)
    VariantIntelligenceReporter().write(report, args.out_dir)

    print("Variant Intelligence klar.")
    print(f"Profiles: {report.total_profiles}")
    print(f"Families: {report.families}")
    print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
