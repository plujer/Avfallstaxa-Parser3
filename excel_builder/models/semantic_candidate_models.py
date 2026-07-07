"""Semantic candidate ranking models."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.tax_semantic_profile_models import TaxSemanticProfile


@dataclass
class SemanticScorePart:
    field: str
    word_value: str
    candidate_value: str
    weight: float
    matched: bool
    score: float
    explanation: str = ""


@dataclass
class SemanticCandidate:
    word_profile: TaxSemanticProfile
    candidate_profile: TaxSemanticProfile
    score: float
    status: str
    score_parts: list[SemanticScorePart] = field(default_factory=list)

    @property
    def explanation(self) -> str:
        matched = [
            f"{part.field}: {part.word_value}"
            for part in self.score_parts
            if part.matched and part.word_value
        ]
        missing = [
            f"{part.field}: Word='{part.word_value}' kandidat='{part.candidate_value}'"
            for part in self.score_parts
            if not part.matched and (part.word_value or part.candidate_value)
        ]

        text = []
        if matched:
            text.append("Matchar " + ", ".join(matched[:6]))
        if missing:
            text.append("Skillnader " + ", ".join(missing[:4]))
        return ". ".join(text)


@dataclass
class SemanticCandidateReport:
    candidates: list[SemanticCandidate] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_candidates(self) -> int:
        return len(self.candidates)

    @property
    def unique_word_profiles(self) -> int:
        return len({candidate.word_profile.source_id for candidate in self.candidates})

    def top_for_word(self, source_id: str, limit: int = 10) -> list[SemanticCandidate]:
        rows = [candidate for candidate in self.candidates if candidate.word_profile.source_id == source_id]
        return sorted(rows, key=lambda item: item.score, reverse=True)[:limit]
