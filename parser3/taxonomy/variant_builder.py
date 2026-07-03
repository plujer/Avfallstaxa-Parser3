"""Build tax variants from headers and cells."""

from __future__ import annotations


class VariantBuilder:
    FREQUENCY_WORDS = [
        "hämtning varje vecka",
        "hämtning var 14:e dag",
        "hämtning månadsvis",
        "avgift per tömning",
        "avgift per besök",
        "avgift per tillfälle",
        "avgift per container per dygn",
        "inom 24 timmar på vardagar",
        "inom 48 timmar på vardagar",
        "inom 7 arbetsdagar",
        "inom 8 arbetsdagar",
    ]

    def from_context(self, group: str = "", header: str = "", cells: list[str] | None = None) -> str:
        cells = cells or []
        joined = " ".join([group, header] + cells).lower()

        for word in self.FREQUENCY_WORDS:
            if word in joined:
                return word[:1].upper() + word[1:]

        return ""
