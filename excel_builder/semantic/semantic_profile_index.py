"""Index and compare semantic tax profiles."""

from __future__ import annotations

from collections import defaultdict

from excel_builder.models import TaxSemanticProfile, TaxSemanticProfileKey


class SemanticProfileIndex:
    def __init__(self, profiles: list[TaxSemanticProfile] | None = None) -> None:
        self.profiles = profiles or []
        self.by_key: dict[TaxSemanticProfileKey, list[TaxSemanticProfile]] = defaultdict(list)
        for profile in self.profiles:
            self.by_key[profile.key].append(profile)

    def candidates(self, profile: TaxSemanticProfile, min_score: float = 0.45) -> list[tuple[TaxSemanticProfile, float]]:
        scored: list[tuple[TaxSemanticProfile, float]] = []

        for candidate in self.profiles:
            score = self.score(profile, candidate)
            if score >= min_score:
                scored.append((candidate, score))

        return sorted(scored, key=lambda item: item[1], reverse=True)

    def score(self, a: TaxSemanticProfile, b: TaxSemanticProfile) -> float:
        weights = {
            "category": 0.14,
            "waste_type": 0.22,
            "service_type": 0.10,
            "container_type": 0.10,
            "container_volume_liter": 0.14,
            "interval": 0.10,
            "property_type": 0.08,
            "unit_type": 0.06,
            "factor_hint": 0.06,
        }

        score = 0.0
        for field, weight in weights.items():
            av = getattr(a.key, field)
            bv = getattr(b.key, field)
            if av and bv and av == bv:
                score += weight

        return round(score, 4)
