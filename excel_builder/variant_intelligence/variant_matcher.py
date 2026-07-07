"""Compare variants inside tax families."""

from __future__ import annotations

from excel_builder.models import TaxVariantProfile, VariantComparison
from excel_builder.variant_intelligence.variant_parser import VariantParser


class VariantMatcher:
    FIELDS = ["volume_liter", "waste_code", "interval", "variant", "usage_type"]

    def __init__(self) -> None:
        self.parser = VariantParser()

    def compare_codes(
        self,
        word_tax_code: str,
        candidate_tax_code: str,
        word_text: str = "",
        candidate_text: str = "",
    ) -> VariantComparison:
        word = self.parser.parse(word_tax_code, word_text, source="WORD")
        candidate = self.parser.parse(candidate_tax_code, candidate_text, source="CANDIDATE")
        return self.compare_profiles(word, candidate)

    def compare_profiles(self, word: TaxVariantProfile, candidate: TaxVariantProfile) -> VariantComparison:
        same_family = bool(word.family_code and candidate.family_code and word.family_code == candidate.family_code)
        matched: list[str] = []
        mismatched: list[str] = []

        for field in self.FIELDS:
            left = getattr(word, field)
            right = getattr(candidate, field)
            if not left or not right:
                continue
            if left == right:
                matched.append(field)
            else:
                mismatched.append(field)

        comparable = len(matched) + len(mismatched)
        field_score = (len(matched) / comparable) if comparable else 0.0
        score = 0.0
        if same_family:
            score += 0.55
        score += field_score * 0.45
        score = round(min(score, 1.0), 4)

        same_variant = same_family and comparable > 0 and not mismatched
        if same_variant:
            explanation = "Samma taxefamilj och inga identifierade variantavvikelser."
        elif same_family:
            explanation = "Samma taxefamilj men identifierade variantavvikelser."
        else:
            explanation = "Olika taxefamiljer. Variantjämförelse ska inte användas som match."

        return VariantComparison(
            word=word,
            candidate=candidate,
            same_family=same_family,
            same_variant=same_variant,
            score=score,
            matched_fields=matched,
            mismatched_fields=mismatched,
            explanation=explanation,
        )

    def bonus(self, word_tax_code: str, candidate_tax_code: str, word_text: str = "", candidate_text: str = "") -> float:
        comparison = self.compare_codes(word_tax_code, candidate_tax_code, word_text, candidate_text)
        if comparison.same_variant:
            return 0.05
        if comparison.same_family:
            return 0.02
        return 0.0
