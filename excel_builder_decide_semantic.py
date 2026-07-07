from __future__ import annotations

import argparse

from excel_builder.context import ParserContextResolver
from excel_builder.decision import DecisionWorkbookWriter, SemanticDecisionEngine
from excel_builder.io import ParserMatchReader
from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.reports import DecisionReporter
from excel_builder.rules import MasterRuleRepositoryReader
from excel_builder.semantic import SemanticCandidateRanker, TaxSemanticProfileEngine
from excel_builder.standard import StandardTaxReader


def main() -> None:
    parser = argparse.ArgumentParser(description="Create final decisions using semantic candidate ranking")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--reference-workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--workbook", required=True)
    parser.add_argument("--municipality", default="")
    parser.add_argument("--txt", default="output/excel/tax_decision_semantic_report.txt")
    parser.add_argument("--csv", default="output/excel/tax_decision_semantic_results.csv")
    args = parser.parse_args()

    original_rows = ParserMatchReader().read(args.parser_result)
    context_report = ParserContextResolver().resolve(original_rows)
    enriched_rows = [item.enriched_row for item in context_report.rows]

    profile_engine = TaxSemanticProfileEngine()
    knowledge_report = TaxKnowledgeExtractor().extract(enriched_rows)
    word_profiles = profile_engine.from_knowledge_report(knowledge_report).profiles

    standard_catalog = StandardTaxReader().read(args.standard_tax)
    standard_profiles = profile_engine.from_standard_catalog(standard_catalog).profiles

    repo = MasterRuleRepositoryReader().read(args.reference_workbook)
    rule_profiles = profile_engine.from_rule_repository(repo).profiles

    candidates = SemanticCandidateRanker().rank(word_profiles, standard_profiles + rule_profiles, top_n=10)
    decisions = SemanticDecisionEngine().decide(original_rows, candidates.candidates)

    DecisionReporter().write_txt(decisions, args.txt)
    DecisionReporter().write_csv(decisions, args.csv)
    DecisionWorkbookWriter().write(args.workbook, decisions, municipality=args.municipality)

    print("Semantic Decision Engine klar")
    print(f"Parser rows: {len(original_rows)}")
    print(f"Context enriched rows: {context_report.enriched_count}")
    print(f"Semantic candidates: {candidates.total_candidates}")
    print(f"EDP_MATCH: {decisions.edp_match}")
    print(f"STANDARD_PROPOSAL: {decisions.standard_proposal}")
    print(f"REVIEW_REQUIRED: {decisions.review_required}")
    print(f"NEW_TAXA: {decisions.new_taxa}")
    print(f"Workbook: {args.workbook}")


if __name__ == "__main__":
    main()
