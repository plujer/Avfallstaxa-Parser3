"""Rank semantic candidates with explainable scoring.

The ranker compares WORD profiles against STANDARD and RULE profiles and returns
the best candidates. It replaces exact-key grouping with weighted similarity.
"""

from __future__ import annotations

from excel_builder.models import (
    SemanticCandidate,
    SemanticCandidateReport,
    SemanticScorePart,
    TaxSemanticProfile,
)


class SemanticCandidateRanker:
    WEIGHTS = {
        "category": 0.14,
        "waste_type": 0.24,
        "service_type": 0.10,
        "container_type": 0.10,
        "container_volume_liter": 0.16,
        "interval": 0.08,
        "property_type": 0.06,
        "unit_type": 0.06,
        "factor_hint": 0.06,
    }

    AUTO_MATCH_THRESHOLD = 0.98
    STANDARD_PROPOSAL_THRESHOLD = 0.88
    REVIEW_THRESHOLD = 0.70

    def rank(
        self,
        word_profiles: list[TaxSemanticProfile],
        candidate_profiles: list[TaxSemanticProfile],
        top_n: int = 10,
    ) -> SemanticCandidateReport:
        report = SemanticCandidateReport()

        allowed_sources = ("STANDARD", "RULE:TAXEPUNKT", "RULE:EDP")
        candidates = [
            profile
            for profile in candidate_profiles
            if profile.source.startswith(allowed_sources)
        ]

        for word in word_profiles:
            ranked = []
            for candidate in candidates:
                score, parts = self.score(word, candidate)
                if score <= 0:
                    continue

                ranked.append(
                    SemanticCandidate(
                        word_profile=word,
                        candidate_profile=candidate,
                        score=score,
                        status=self.status_for_score(score, candidate),
                        score_parts=parts,
                    )
                )

            ranked.sort(key=lambda item: item.score, reverse=True)
            report.candidates.extend(ranked[:top_n])

        return report

    def score(self, word: TaxSemanticProfile, candidate: TaxSemanticProfile) -> tuple[float, list[SemanticScorePart]]:
        total = 0.0
        parts: list[SemanticScorePart] = []

        for field, weight in self.WEIGHTS.items():
            word_value = getattr(word.key, field)
            candidate_value = getattr(candidate.key, field)

            matched = bool(word_value and candidate_value and word_value == candidate_value)
            # If Word is missing a property but the candidate has it, do not penalize fully:
            # unknown Word data should not block strong candidates.
            partial = False
            if not matched and not word_value and candidate_value:
                partial = True

            if matched:
                part_score = weight
                explanation = "match"
            elif partial:
                part_score = weight * 0.25
                explanation = "word saknar värde"
            else:
                part_score = 0.0
                explanation = "avvikelse"

            total += part_score
            parts.append(
                SemanticScorePart(
                    field=field,
                    word_value=word_value,
                    candidate_value=candidate_value,
                    weight=weight,
                    matched=matched,
                    score=part_score,
                    explanation=explanation,
                )
            )

        return round(total, 4), parts

    def status_for_score(self, score: float, candidate: TaxSemanticProfile) -> str:
        if score >= self.AUTO_MATCH_THRESHOLD and candidate.source.startswith("RULE:"):
            return "EDP_MATCH"
        if score >= self.STANDARD_PROPOSAL_THRESHOLD:
            return "STANDARD_PROPOSAL" if candidate.source == "STANDARD" else "RULE_PROPOSAL"
        if score >= self.REVIEW_THRESHOLD:
            return "REVIEW_REQUIRED"
        return "LOW_CONFIDENCE"
