from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.reports import SemanticProfileReporter
from excel_builder.rules import MasterRuleRepositoryReader
from excel_builder.semantic import TaxSemanticProfileEngine
from excel_builder.standard import StandardTaxReader


def main() -> None:
    parser = argparse.ArgumentParser(description="Build semantic tax profiles")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--txt", default="output/excel/semantic_profile_report.txt")
    parser.add_argument("--csv", default="output/excel/semantic_profiles.csv")
    args = parser.parse_args()

    engine = TaxSemanticProfileEngine()

    parser_rows = ParserMatchReader().read(args.parser_result)
    knowledge_report = TaxKnowledgeExtractor().extract(parser_rows)
    word_profiles = engine.from_knowledge_report(knowledge_report)

    standard_catalog = StandardTaxReader().read(args.standard_tax)
    standard_profiles = engine.from_standard_catalog(standard_catalog)

    repo = MasterRuleRepositoryReader().read(args.workbook)
    rule_profiles = engine.from_rule_repository(repo)

    combined = word_profiles
    combined.profiles.extend(standard_profiles.profiles)
    combined.profiles.extend(rule_profiles.profiles)
    combined.warnings.extend(standard_profiles.warnings)
    combined.warnings.extend(rule_profiles.warnings)

    txt = SemanticProfileReporter().write_txt(combined, args.txt)
    csv = SemanticProfileReporter().write_csv(combined, args.csv)

    print("Tax Semantic Profiles klar")
    print(f"Word profiles: {len(word_profiles.by_source('WORD'))}")
    print(f"Standard profiles: {len(standard_profiles.by_source('STANDARD'))}")
    print(f"Rule profiles: {len(rule_profiles.profiles)}")
    print(f"Total profiles: {combined.total}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
