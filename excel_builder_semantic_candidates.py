from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.reports import SemanticCandidateReporter
from excel_builder.rules import MasterRuleRepositoryReader
from excel_builder.semantic import SemanticCandidateRanker, TaxSemanticProfileEngine
from excel_builder.standard import StandardTaxReader


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank semantic tax candidates")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", default="data/ArbetsExcel_Reference.xlsx")
    parser.add_argument("--txt", default="output/excel/semantic_candidate_report.txt")
    parser.add_argument("--csv", default="output/excel/semantic_candidates.csv")
    parser.add_argument("--top-n", type=int, default=10)
    args = parser.parse_args()

    engine = TaxSemanticProfileEngine()

    parser_rows = ParserMatchReader().read(args.parser_result)
    knowledge_report = TaxKnowledgeExtractor().extract(parser_rows)
    word_profiles = engine.from_knowledge_report(knowledge_report).profiles

    standard_catalog = StandardTaxReader().read(args.standard_tax)
    standard_profiles = engine.from_standard_catalog(standard_catalog).profiles

    repo = MasterRuleRepositoryReader().read(args.workbook)
    rule_profiles = engine.from_rule_repository(repo).profiles

    candidate_profiles = standard_profiles + rule_profiles
    report = SemanticCandidateRanker().rank(word_profiles, candidate_profiles, top_n=args.top_n)

    txt = SemanticCandidateReporter().write_txt(report, args.txt)
    csv = SemanticCandidateReporter().write_csv(report, args.csv)

    print("Semantic Candidate Ranking klar")
    print(f"Word profiles: {len(word_profiles)}")
    print(f"Candidate profiles: {len(candidate_profiles)}")
    print(f"Total candidates returned: {report.total_candidates}")
    print(f"Word profiles with candidates: {report.unique_word_profiles}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
