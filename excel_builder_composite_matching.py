"""CLI for Composite Matching Engine."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.composite_matching import CompositeMatchingRepository
from excel_builder.reports.composite_matching_reporter import CompositeMatchingReporter
from excel_builder.rules.master_rule_repository_reader import MasterRuleRepositoryReader
from excel_builder.standard.standard_tax_reader import StandardTaxReader


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Composite Matching Engine reports.")
    parser.add_argument("--standard-tax", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()

    catalog = StandardTaxReader().read(Path(args.standard_tax))
    repository = MasterRuleRepositoryReader().read(Path(args.workbook))
    report = CompositeMatchingRepository().from_standard_and_rules(catalog, repository, limit=args.limit)
    CompositeMatchingReporter().write(report, args.out_dir)

    print("Composite Matching Engine klar.")
    print(f"Results: {report.total_results}")
    print(f"MATCH: {report.ok_count}")
    print(f"REVIEW: {report.review_count}")
    print(f"NO_MATCH: {report.no_match_count}")
    print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
