"""Explain whether two tax codes belong to the same tax family."""

from __future__ import annotations

from excel_builder.models import TaxFamilyMatch
from excel_builder.tax_family.tax_family_parser import TaxFamilyParser


class TaxFamilyMatcher:
    def __init__(self) -> None:
        self.parser = TaxFamilyParser()

    def compare(self, word_tax_code: str, candidate_tax_code: str) -> TaxFamilyMatch:
        word = self.parser.parse_member(word_tax_code, source="WORD")
        candidate = self.parser.parse_member(candidate_tax_code, source="CANDIDATE")

        word_family = word.family_key.value
        candidate_family = candidate.family_key.value
        same_family = bool(word_family and candidate_family and word_family == candidate_family)
        same_variant = same_family and (word.variant_key == candidate.variant_key)

        if same_variant:
            explanation = "Samma taxefamilj och samma variant/intervall."
        elif same_family:
            explanation = "Samma taxefamilj men annan variant/intervall."
        else:
            explanation = "Olika taxefamiljer."

        return TaxFamilyMatch(
            word_tax_code=word_tax_code,
            candidate_tax_code=candidate_tax_code,
            word_family=word_family,
            candidate_family=candidate_family,
            same_family=same_family,
            same_variant=same_variant,
            explanation=explanation,
        )

    def bonus(self, word_tax_code: str, candidate_tax_code: str) -> float:
        match = self.compare(word_tax_code, candidate_tax_code)
        if match.same_variant:
            return 0.04
        if match.same_family:
            return 0.025
        return 0.0
