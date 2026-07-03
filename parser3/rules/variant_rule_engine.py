"""Rules for known variant patterns."""

from __future__ import annotations


class VariantRuleEngine:
    VARIANTS = [
        "Hämtning varje vecka",
        "Hämtning var 14:e dag",
        "Hämtning månadsvis",
        "Avgift per tömning",
        "Avgift per lägenhet",
        "Avgift per besök",
        "Avgift per container per dygn",
        "Inom 24 timmar på vardagar",
        "Inom 48 timmar på vardagar",
        "Inom 7 arbetsdagar",
        "Inom 8 arbetsdagar",
    ]

    def find_variant(self, text: str) -> str:
        lower = (text or "").lower()
        for variant in self.VARIANTS:
            if variant.lower() in lower:
                return variant
        return ""
