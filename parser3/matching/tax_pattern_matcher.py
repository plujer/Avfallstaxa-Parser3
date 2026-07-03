"""Pattern matcher for tax rows against golden master rows."""

from __future__ import annotations

from difflib import SequenceMatcher

from parser3.models import TaxRow


class TaxPatternMatcher:
    def similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()

    def best_match(self, row: TaxRow, facit_rows: list[dict]) -> tuple[dict | None, float]:
        best = None
        best_score = 0.0

        for facit in facit_rows:
            name_score = self.similarity(row.name, facit.get("name", ""))
            unit_score = 1.0 if row.unit == facit.get("unit", "") else 0.0
            variant_score = 1.0 if row.variant == facit.get("variant", "") else 0.0
            score = (name_score * 0.7) + (unit_score * 0.2) + (variant_score * 0.1)
            if score > best_score:
                best = facit
                best_score = score

        return best, best_score
