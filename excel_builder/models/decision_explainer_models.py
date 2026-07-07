"""Explainable decision engine models.

The explainable decision layer converts composite matching output into a
human-readable decision trace. It is conservative decision support only:
Taxa_från_edp remains the source of truth and is never modified.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DecisionTracePart:
    signal: str
    score: float
    weight: float
    contribution: float
    explanation: str = ""


@dataclass(frozen=True)
class DecisionTrace:
    word_tax_code: str
    candidate_tax_code: str
    decision: str
    confidence: float
    total_score: float
    primary_reason: str
    parts: list[DecisionTracePart] = field(default_factory=list)
    rejected_reason: str = ""


@dataclass
class ExplainableDecisionReport:
    traces: list[DecisionTrace] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_traces(self) -> int:
        return len(self.traces)

    @property
    def accepted_count(self) -> int:
        return sum(1 for trace in self.traces if trace.decision == "ACCEPT")

    @property
    def review_count(self) -> int:
        return sum(1 for trace in self.traces if trace.decision == "REVIEW")

    @property
    def rejected_count(self) -> int:
        return sum(1 for trace in self.traces if trace.decision == "REJECT")
