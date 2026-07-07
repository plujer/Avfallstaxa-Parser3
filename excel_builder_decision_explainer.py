"""CLI for Explainable Decision Engine."""

from __future__ import annotations

import argparse
from pathlib import Path

from excel_builder.composite_matching import CompositeMatchingRepository
from excel_builder.decision_explainer import ExplainableDecisionEngine
from excel_builder.reports.decision_explainer_reporter import DecisionExplainerReporter
from excel_builder.rules.master_rule_repository_reader import MasterRuleRepositoryReader
from excel_builder.standard.standard_tax_reader import StandardTaxReader


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Explainable Decision Engine reports.")
    parser.add_argument("--standard-tax", required=True)
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--out-dir", default="output/excel")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()

    catalog = StandardTaxReader().read(Path(args.standard_tax))
    repository = MasterRuleRepositoryReader().read(Path(args.workbook))
    composite_report = CompositeMatchingRepository().from_standard_and_rules(catalog, repository, limit=args.limit)
    report = ExplainableDecisionEngine().explain(composite_report)
    DecisionExplainerReporter().write(report, args.out_dir)

    print("Explainable Decision Engine klar.")
    print(f"Traces: {report.total_traces}")
    print(f"ACCEPT: {report.accepted_count}")
    print(f"REVIEW: {report.review_count}")
    print(f"REJECT: {report.rejected_count}")
    print(f"Warnings: {len(report.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
