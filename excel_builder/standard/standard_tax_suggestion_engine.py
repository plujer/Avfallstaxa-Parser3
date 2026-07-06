"""Suggest missing tax codes from the EDP standard tax catalog.

Standard tax suggestions are never treated as confirmed EDP codes. They are
review material for Taxa_Förslag.
"""

from __future__ import annotations

from difflib import SequenceMatcher

from excel_builder.knowledge import TaxKnowledgeExtractor
from excel_builder.matching import MatchNormalizer
from excel_builder.models import (
    ParserTaxRow,
    StandardTaxCatalog,
    StandardTaxRow,
    StandardTaxSuggestion,
    StandardTaxSuggestionReport,
)
from excel_builder.standard.knowledge_based_standard_matcher import KnowledgeBasedStandardMatcher


class StandardTaxSuggestionEngine:
    PROPOSAL_THRESHOLD = 0.86
    REVIEW_THRESHOLD = 0.70

    def __init__(self, use_knowledge_matching: bool = True) -> None:
        self.normalizer = MatchNormalizer()
        self.use_knowledge_matching = use_knowledge_matching
        self.knowledge_extractor = TaxKnowledgeExtractor()
        self.knowledge_matcher = KnowledgeBasedStandardMatcher()

    def suggest(self, parser_rows: list[ParserTaxRow], catalog: StandardTaxCatalog) -> StandardTaxSuggestionReport:
        if self.use_knowledge_matching:
            return self._suggest_with_knowledge(parser_rows, catalog)

        return self._suggest_with_text_similarity(parser_rows, catalog)

    def _suggest_with_knowledge(self, parser_rows: list[ParserTaxRow], catalog: StandardTaxCatalog) -> StandardTaxSuggestionReport:
        report = StandardTaxSuggestionReport()
        report.warnings.extend(catalog.warnings)

        features = self.knowledge_extractor.extract(parser_rows).features
        matches = self.knowledge_matcher.match(features, catalog)

        for match in matches:
            if match.status == "PROPOSAL":
                comment = f"Kunskapsbaserad standardträff. {match.explanation}"
            elif match.status == "REVIEW":
                comment = f"Möjlig kunskapsbaserad standardträff. {match.explanation}"
            else:
                comment = match.explanation

            report.suggestions.append(
                StandardTaxSuggestion(
                    parser_row=match.feature.parser_row,
                    standard_row=match.standard_row,
                    status=match.status,
                    score=match.score,
                    method=match.rule,
                    comment=comment,
                )
            )

        return report

    def _suggest_with_text_similarity(self, parser_rows: list[ParserTaxRow], catalog: StandardTaxCatalog) -> StandardTaxSuggestionReport:
        report = StandardTaxSuggestionReport()
        report.warnings.extend(catalog.warnings)

        for parser_row in parser_rows:
            best = self._best_match(parser_row, catalog.rows)

            if best is None:
                report.suggestions.append(
                    StandardTaxSuggestion(
                        parser_row=parser_row,
                        standard_row=None,
                        status="NO_SUGGESTION",
                        score=0.0,
                        method="no standard catalog rows",
                        comment="Ingen standardtaxekatalog att matcha mot",
                    )
                )
                continue

            standard_row, score = best

            if score >= self.PROPOSAL_THRESHOLD:
                status = "PROPOSAL"
                comment = "Stark standardtaxeträff. Ska granskas innan användning."
            elif score >= self.REVIEW_THRESHOLD:
                status = "REVIEW"
                comment = "Möjlig standardtaxeträff. Kräver manuell granskning."
            else:
                status = "NO_SUGGESTION"
                comment = "Ingen tillräckligt stark standardtaxeträff."

            report.suggestions.append(
                StandardTaxSuggestion(
                    parser_row=parser_row,
                    standard_row=standard_row if status != "NO_SUGGESTION" else None,
                    status=status,
                    score=score,
                    method="standard strTaxebenamning similarity",
                    comment=comment,
                )
            )

        return report

    def _best_match(self, parser_row: ParserTaxRow, standard_rows: list[StandardTaxRow]) -> tuple[StandardTaxRow, float] | None:
        parser_name = self.normalizer.normalize(parser_row.tax_point)
        parser_unit = self.normalizer.normalize(parser_row.unit)

        best_row: StandardTaxRow | None = None
        best_score = 0.0

        for standard_row in standard_rows:
            standard_name = self.normalizer.normalize(standard_row.strTaxebenamning)
            if not standard_name:
                continue

            name_score = SequenceMatcher(None, parser_name, standard_name).ratio()

            combined_standard = self.normalizer.normalize(
                " ".join([
                    standard_row.strTaxebenamning,
                    standard_row.strTaxedelAvser,
                    standard_row.strFaktor,
                    standard_row.strFormel,
                ])
            )
            unit_boost = 0.03 if parser_unit and parser_unit in combined_standard else 0.0
            score = min(name_score + unit_boost, 1.0)

            if score > best_score:
                best_score = score
                best_row = standard_row

        if best_row is None:
            return None
        return best_row, best_score
