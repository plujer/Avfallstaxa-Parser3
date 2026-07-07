"""Build detailed decision traces from composite matching results."""

from __future__ import annotations

from excel_builder.decision_explainer.confidence_calculator import ConfidenceCalculator
from excel_builder.models import CompositeMatchResult, DecisionTrace, DecisionTracePart


class DecisionTraceBuilder:
    def __init__(self) -> None:
        self.confidence_calculator = ConfidenceCalculator()

    def build(self, result: CompositeMatchResult) -> DecisionTrace:
        confidence = self.confidence_calculator.calculate(result)
        decision = self._decision(result, confidence)
        parts = [
            DecisionTracePart(
                signal=part.name,
                score=round(part.score, 4),
                weight=round(part.weight, 4),
                contribution=round(part.weighted_score, 4),
                explanation=part.explanation,
            )
            for part in result.parts
        ]
        primary = self._primary_reason(result)
        rejected = "" if decision != "REJECT" else "Samlad poäng och confidence är för låg för automatisk accept."
        return DecisionTrace(
            word_tax_code=result.word_tax_code,
            candidate_tax_code=result.candidate_tax_code,
            decision=decision,
            confidence=confidence,
            total_score=round(result.score, 4),
            primary_reason=primary,
            parts=parts,
            rejected_reason=rejected,
        )

    def _decision(self, result: CompositeMatchResult, confidence: float) -> str:
        if result.status == "MATCH" and confidence >= 0.70:
            return "ACCEPT"
        if result.status in {"MATCH", "REVIEW"} and confidence >= 0.35:
            return "REVIEW"
        return "REJECT"

    def _primary_reason(self, result: CompositeMatchResult) -> str:
        if not result.parts:
            return "Inga poängdelar finns att förklara."
        strongest = sorted(result.parts, key=lambda part: part.weighted_score, reverse=True)[:3]
        return "; ".join(
            f"{part.name} bidrar {part.weighted_score:.4f}: {part.explanation}" for part in strongest
        )
