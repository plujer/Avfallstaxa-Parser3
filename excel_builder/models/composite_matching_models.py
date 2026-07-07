"""Composite matching models.

Composite matching combines conservative decision-support signals from document
structure, hierarchical context, tax family intelligence, variant intelligence,
semantic attributes, EDP matches and standard-tax proposals. It never modifies
Taxa_från_edp or municipality-specific project data.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CompositeScorePart:
    name: str
    score: float
    weight: float
    explanation: str = ""

    @property
    def weighted_score(self) -> float:
        return round(max(0.0, min(1.0, self.score)) * self.weight, 4)


@dataclass(frozen=True)
class CompositeMatchInput:
    word_tax_code: str = ""
    candidate_tax_code: str = ""
    word_text: str = ""
    candidate_text: str = ""
    edp_exact_match: bool = False
    standard_proposal: bool = False
    same_context: bool = False
    same_structure: bool = False
    source: str = ""


@dataclass(frozen=True)
class CompositeMatchResult:
    word_tax_code: str
    candidate_tax_code: str
    score: float
    status: str
    parts: list[CompositeScorePart] = field(default_factory=list)
    explanation: str = ""

    @property
    def weighted_total(self) -> float:
        return round(sum(part.weighted_score for part in self.parts), 4)


@dataclass
class CompositeMatchingReport:
    results: list[CompositeMatchResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_results(self) -> int:
        return len(self.results)

    @property
    def ok_count(self) -> int:
        return sum(1 for result in self.results if result.status == "MATCH")

    @property
    def review_count(self) -> int:
        return sum(1 for result in self.results if result.status == "REVIEW")

    @property
    def no_match_count(self) -> int:
        return sum(1 for result in self.results if result.status == "NO_MATCH")
