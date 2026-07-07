"""Parse EDP tax codes into semantic parts.

This is intentionally conservative. Unknown parts are preserved in suffix/notes.
The parser does not decide or modify EDP; it extracts reusable knowledge.
"""

from __future__ import annotations

import re

from excel_builder.models import ParsedTaxCode


class TaxCodeParser:
    PREFIX_MAP = {
        "KÄ": "Kärl",
        "KA": "Kärl",
        "SÄ": "Säck",
        "SA": "Säck",
        "CON": "Container",
        "SL": "Slam",
        "SLA": "Slam",
        "FA": "Farligt avfall",
    }

    WASTE_MAP = {
        "RM": "Rest-/matavfall",
        "RE": "Restavfall",
        "MA": "Matavfall",
        "PL": "Plastförpackningar",
        "PA": "Pappersförpackningar",
        "GF": "Glasförpackningar färgat",
        "GO": "Glasförpackningar ofärgat",
        "ME": "Metallförpackningar",
        "TI": "Tidningar",
        "ASB": "Asbest",
        "GIP": "Gips",
        "TR": "Träavfall",
    }

    VARIANT_HINTS = {
        "FV": "Fritidsvariant",
        "FRI": "Fritid",
        "EX": "Extra",
        "LÅS": "Lås",
        "LAS": "Lås",
    }

    def parse(self, code: str) -> ParsedTaxCode:
        original = str(code or "").strip()
        normalized = original.upper().replace(" ", "").replace("-", "")
        parsed = ParsedTaxCode(original_code=original)

        if not normalized:
            parsed.notes.append("Tom taxekod.")
            return parsed

        parsed.prefix = self._prefix(normalized)
        parsed.container_type = self.PREFIX_MAP.get(parsed.prefix, "")

        remaining = normalized[len(parsed.prefix):] if parsed.prefix else normalized

        volume_match = re.match(r"(\d{2,4})", remaining)
        if volume_match:
            parsed.volume_liter = volume_match.group(1)
            remaining = remaining[len(parsed.volume_liter):]

        waste = self._waste_code(remaining)
        if waste:
            parsed.waste_code = waste
            parsed.waste_type = self.WASTE_MAP.get(waste, "")
            remaining = remaining[len(waste):]

        interval_match = re.match(r"(\d{1,3})", remaining)
        if interval_match:
            parsed.interval = interval_match.group(1)
            remaining = remaining[len(parsed.interval):]

        variant = self._variant(remaining)
        if variant:
            parsed.variant = variant
            remaining = remaining[len(variant):]

        parsed.suffix = remaining
        parsed.confidence = self._confidence(parsed)

        if parsed.suffix:
            parsed.notes.append(f"Okänd suffix: {parsed.suffix}")
        if not parsed.prefix:
            parsed.notes.append("Kunde inte identifiera prefix.")
        if parsed.prefix in {"KÄ", "KA"} and not parsed.volume_liter:
            parsed.notes.append("Kärlkod saknar identifierad volym.")

        return parsed

    def parse_many(self, codes: list[str]) -> list[ParsedTaxCode]:
        return [self.parse(code) for code in codes]

    def _prefix(self, normalized: str) -> str:
        for prefix in sorted(self.PREFIX_MAP, key=len, reverse=True):
            if normalized.startswith(prefix):
                return prefix
        return ""

    def _waste_code(self, remaining: str) -> str:
        for waste in sorted(self.WASTE_MAP, key=len, reverse=True):
            if remaining.startswith(waste):
                return waste
        return ""

    def _variant(self, remaining: str) -> str:
        for variant in sorted(self.VARIANT_HINTS, key=len, reverse=True):
            if remaining.startswith(variant):
                return variant
        # If only letters remain, treat as variant rather than unknown numeric interval.
        if remaining and remaining.isalpha():
            return remaining
        return ""

    def _confidence(self, parsed: ParsedTaxCode) -> float:
        score = 0.0
        if parsed.prefix:
            score += 0.25
        if parsed.container_type:
            score += 0.15
        if parsed.volume_liter:
            score += 0.20
        if parsed.waste_code:
            score += 0.20
        if parsed.interval:
            score += 0.10
        if parsed.variant:
            score += 0.05
        if not parsed.suffix:
            score += 0.05
        return min(score, 1.0)
