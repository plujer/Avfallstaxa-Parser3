"""Confidence calculation for explainable decisions."""

from __future__ import annotations

from excel_builder.models import CompositeMatchResult


class ConfidenceCalculator:
    """Calculates a conservative confidence score from composite signals."""

    def calculate(self, result: CompositeMatchResult) -> float:
        score = max(0.0, min(1.0, float(result.score or 0.0)))
        positive_parts = [part for part in result.parts if part.score >= 0.75]
        weak_parts = [part for part in result.parts if part.score <= 0.25]
        confidence = score
        if any(part.name == "edp_exact" and part.score >= 1.0 for part in result.parts):
            confidence += 0.08
        if len(positive_parts) >= 3:
            confidence += 0.05
        if len(weak_parts) >= 4:
            confidence -= 0.08
        return round(max(0.0, min(1.0, confidence)), 4)
