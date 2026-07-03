"""Confidence scoring for extracted rows."""

from __future__ import annotations

from parser3.models import TaxRow


class ConfidenceScoring:
    def score(self, row: TaxRow) -> float:
        score = 0.0
        if row.name:
            score += 0.35
        if row.section:
            score += 0.20
        if row.unit:
            score += 0.20
        if row.price:
            score += 0.10
        if row.ewc or row.un_number:
            score += 0.15
        return min(score, 1.0)
