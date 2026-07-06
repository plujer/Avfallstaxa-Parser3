"""Detect table shape from header rows."""

from __future__ import annotations


class TableShapeDetector:
    FREQUENCY_HEADERS = {
        "varje vecka": "Hämtning varje vecka",
        "var 14:e dag": "Hämtning var 14:e dag",
        "månadsvis": "Hämtning månadsvis",
    }

    UNIT_HEADERS = {
        "avgift per besök": "besök",
        "avgift per kg": "kilogram",
        "avgift per lyft": "lyft",
        "avgift per tömning": "tömning",
        "avgift per lägenhet": "lägenhet",
        "avgift per faktura": "faktura",
        "avgift per kärl": "kärl",
        "avgift per st": "styck",
        "avgift per styck": "styck",
        "avgift per tillfälle": "tillfälle",
        "avgift per container": "container",
    }

    def is_header(self, cells: list[str]) -> bool:
        text = " ".join(cells).lower()
        tokens = ["typ av", "avgift", "pris", "enhet", "ewc", "un-nr", "hämtning"]
        return sum(1 for token in tokens if token in text) >= 1 and "kr" not in text

    def variants_from_header(self, cells: list[str]) -> dict[int, str]:
        variants: dict[int, str] = {}
        for idx, cell in enumerate(cells):
            lower = (cell or "").lower()
            for token, variant in self.FREQUENCY_HEADERS.items():
                if token in lower:
                    variants[idx] = variant
        return variants

    def unit_from_header(self, cells: list[str]) -> str:
        text = " ".join(cells).lower()
        for token, unit in self.UNIT_HEADERS.items():
            if token in text:
                return unit
        return ""
