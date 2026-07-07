"""Composite Matching Engine.

This engine combines existing conservative signals into one explainable score.
It is decision support only. Taxa_från_edp remains the source of truth.
"""

from __future__ import annotations

from excel_builder.models import CompositeMatchInput, CompositeMatchResult, CompositeScorePart
from excel_builder.semantic_attributes import SemanticAttributeMatcher
from excel_builder.semantic_attributes.attribute_extractor import SemanticAttributeExtractor
from excel_builder.tax_family import TaxFamilyMatcher
from excel_builder.variant_intelligence import VariantMatcher


class CompositeMatcher:
    WEIGHTS = {
        "edp_exact": 0.30,
        "tax_family": 0.15,
        "variant": 0.20,
        "semantic_attributes": 0.20,
        "hierarchical_context": 0.10,
        "document_structure": 0.05,
    }

    def __init__(self) -> None:
        self.family_matcher = TaxFamilyMatcher()
        self.variant_matcher = VariantMatcher()
        self.attribute_extractor = SemanticAttributeExtractor()
        self.attribute_matcher = SemanticAttributeMatcher()

    def compare(self, item: CompositeMatchInput) -> CompositeMatchResult:
        parts: list[CompositeScorePart] = []

        parts.append(
            CompositeScorePart(
                "edp_exact",
                1.0 if item.edp_exact_match else 0.0,
                self.WEIGHTS["edp_exact"],
                "Direkt träff mot Taxa_från_edp." if item.edp_exact_match else "Ingen direkt EDP-träff.",
            )
        )

        family = self.family_matcher.compare(item.word_tax_code, item.candidate_tax_code)
        family_score = 1.0 if family.same_variant else 0.75 if family.same_family else 0.0
        parts.append(CompositeScorePart("tax_family", family_score, self.WEIGHTS["tax_family"], family.explanation))

        variant = self.variant_matcher.compare_codes(
            item.word_tax_code,
            item.candidate_tax_code,
            item.word_text,
            item.candidate_text,
        )
        parts.append(CompositeScorePart("variant", variant.score, self.WEIGHTS["variant"], variant.explanation))

        word_attrs = self.attribute_extractor.extract(item.word_text or item.word_tax_code, item.word_tax_code, source="WORD")
        candidate_attrs = self.attribute_extractor.extract(
            item.candidate_text or item.candidate_tax_code,
            item.candidate_tax_code,
            source="CANDIDATE",
        )
        attr = self.attribute_matcher.compare(word_attrs, candidate_attrs)
        parts.append(
            CompositeScorePart(
                "semantic_attributes",
                attr.score,
                self.WEIGHTS["semantic_attributes"],
                attr.explanation,
            )
        )

        parts.append(
            CompositeScorePart(
                "hierarchical_context",
                1.0 if item.same_context else 0.0,
                self.WEIGHTS["hierarchical_context"],
                "Samma hierarkiska kontext." if item.same_context else "Ingen verifierad gemensam kontext.",
            )
        )
        parts.append(
            CompositeScorePart(
                "document_structure",
                1.0 if item.same_structure else 0.0,
                self.WEIGHTS["document_structure"],
                "Samma dokumentstruktur." if item.same_structure else "Ingen verifierad gemensam dokumentstruktur.",
            )
        )

        score = round(sum(part.weighted_score for part in parts), 4)
        status = self._status(score, item)
        explanation = self._explain(status, parts)
        return CompositeMatchResult(
            word_tax_code=item.word_tax_code,
            candidate_tax_code=item.candidate_tax_code,
            score=score,
            status=status,
            parts=parts,
            explanation=explanation,
        )

    def _status(self, score: float, item: CompositeMatchInput) -> str:
        if item.edp_exact_match and score >= 0.70:
            return "MATCH"
        if score >= 0.65:
            return "MATCH"
        if score >= 0.35 or item.standard_proposal:
            return "REVIEW"
        return "NO_MATCH"

    def _explain(self, status: str, parts: list[CompositeScorePart]) -> str:
        strongest = sorted(parts, key=lambda part: part.weighted_score, reverse=True)[:3]
        reasons = "; ".join(f"{part.name}={part.score:.2f}" for part in strongest)
        return f"{status}: samlad poäng bygger främst på {reasons}."
