"""Compare semantic attribute profiles for decision support."""

from __future__ import annotations

from excel_builder.models import SemanticAttributeComparison, SemanticAttributeProfile


class SemanticAttributeMatcher:
    FIELDS = (
        "materials",
        "waste_types",
        "units",
        "container_types",
        "intervals",
        "property_types",
    )

    def compare(self, word: SemanticAttributeProfile, candidate: SemanticAttributeProfile) -> SemanticAttributeComparison:
        matched: list[str] = []
        missing: list[str] = []
        score_parts: list[float] = []

        for field in self.FIELDS:
            word_values = set(getattr(word, field))
            candidate_values = set(getattr(candidate, field))
            if not word_values and not candidate_values:
                continue
            if word_values and candidate_values:
                overlap = word_values & candidate_values
                if overlap:
                    matched.extend(f"{field}:{value}" for value in sorted(overlap))
                    score_parts.append(len(overlap) / max(len(word_values), len(candidate_values)))
                else:
                    missing.append(field)
                    score_parts.append(0.0)
            elif word_values and not candidate_values:
                missing.append(field)
                score_parts.append(0.0)

        score = round(sum(score_parts) / len(score_parts), 4) if score_parts else 0.0
        explanation = "Attributmatchning saknar gemensamma attribut."
        if matched:
            explanation = "Matchande attribut: " + ", ".join(matched)
        return SemanticAttributeComparison(
            word=word,
            candidate=candidate,
            score=score,
            matched_attributes=matched,
            missing_attributes=missing,
            explanation=explanation,
        )
