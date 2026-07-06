"""Knowledge-based standard tax matching.

This matcher improves on plain text similarity by using Tax Knowledge features:
category, waste type, unit type, factor hint, section group and keywords.

Important:
Standard tax matches are still suggestions only. They must never overwrite an
existing municipality EDP tax in Taxa_från_edp.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

from excel_builder.matching import MatchNormalizer
from excel_builder.models import StandardTaxCatalog, StandardTaxRow, TaxKnowledgeFeature


@dataclass
class KnowledgeStandardMatch:
    feature: TaxKnowledgeFeature
    standard_row: StandardTaxRow | None
    status: str
    score: float
    rule: str
    explanation: str


class KnowledgeBasedStandardMatcher:
    PROPOSAL_THRESHOLD = 0.72
    REVIEW_THRESHOLD = 0.58

    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def match(self, features: list[TaxKnowledgeFeature], catalog: StandardTaxCatalog) -> list[KnowledgeStandardMatch]:
        matches: list[KnowledgeStandardMatch] = []

        for feature in features:
            best = self._best_match(feature, catalog.rows)

            if best is None:
                matches.append(
                    KnowledgeStandardMatch(
                        feature=feature,
                        standard_row=None,
                        status="NO_SUGGESTION",
                        score=0.0,
                        rule="No catalog rows",
                        explanation="Ingen standardtaxekatalog kunde användas.",
                    )
                )
                continue

            standard_row, score, explanation = best

            if score >= self.PROPOSAL_THRESHOLD:
                status = "PROPOSAL"
            elif score >= self.REVIEW_THRESHOLD:
                status = "REVIEW"
            else:
                status = "NO_SUGGESTION"
                standard_row = None

            matches.append(
                KnowledgeStandardMatch(
                    feature=feature,
                    standard_row=standard_row,
                    status=status,
                    score=score,
                    rule="Knowledge weighted standard match",
                    explanation=explanation if standard_row else "Ingen tillräckligt stark kunskapsträff.",
                )
            )

        return matches

    def _best_match(self, feature: TaxKnowledgeFeature, standard_rows: list[StandardTaxRow]) -> tuple[StandardTaxRow, float, str] | None:
        best_row: StandardTaxRow | None = None
        best_score = 0.0
        best_explanation = ""

        for standard_row in standard_rows:
            score, explanation = self._score(feature, standard_row)
            if score > best_score:
                best_score = score
                best_row = standard_row
                best_explanation = explanation

        if best_row is None:
            return None
        return best_row, best_score, best_explanation

    def _score(self, feature: TaxKnowledgeFeature, standard_row: StandardTaxRow) -> tuple[float, str]:
        parser_name = self.normalizer.normalize(feature.parser_row.tax_point)
        standard_name = self.normalizer.normalize(standard_row.strTaxebenamning)

        standard_combined = self.normalizer.normalize(" ".join([
            standard_row.strTaxekod,
            standard_row.strTaxebenamning,
            standard_row.strFaktor,
            standard_row.strTaxedelAvser,
            standard_row.strFormel,
            standard_row.source_sheet,
        ]))

        score = 0.0
        parts: list[str] = []

        name_score = SequenceMatcher(None, parser_name, standard_name).ratio() if parser_name and standard_name else 0.0
        score += name_score * 0.35
        parts.append(f"namn={name_score:.2f}*0.35")

        keyword_score = self._keyword_overlap(feature.keywords, standard_combined)
        score += keyword_score * 0.20
        parts.append(f"nyckelord={keyword_score:.2f}*0.20")

        waste_score = 1.0 if feature.waste_type and self.normalizer.normalize(feature.waste_type) in standard_combined else 0.0
        score += waste_score * 0.15
        parts.append(f"avfallstyp={waste_score:.2f}*0.15")

        factor_score = 1.0 if feature.factor_hint and self.normalizer.normalize(feature.factor_hint) in standard_combined else 0.0
        score += factor_score * 0.15
        parts.append(f"faktor={factor_score:.2f}*0.15")

        category_score = self._category_score(feature, standard_row)
        score += category_score * 0.10
        parts.append(f"kategori={category_score:.2f}*0.10")

        unit_score = self._unit_score(feature, standard_combined)
        score += unit_score * 0.05
        parts.append(f"enhet={unit_score:.2f}*0.05")

        return min(score, 1.0), " | ".join(parts)

    def _keyword_overlap(self, keywords: list[str], standard_combined: str) -> float:
        if not keywords:
            return 0.0

        hits = 0
        usable = 0
        for keyword in keywords:
            if len(keyword) < 4:
                continue
            usable += 1
            if self.normalizer.normalize(keyword) in standard_combined:
                hits += 1

        if usable == 0:
            return 0.0
        return hits / usable

    def _category_score(self, feature: TaxKnowledgeFeature, standard_row: StandardTaxRow) -> float:
        source = self.normalizer.normalize(standard_row.source_sheet)
        category = self.normalizer.normalize(feature.category)

        if "åvc" in category or "verksamhetsavfall" in category:
            return 1.0 if "avfall" in source else 0.0
        if "slam" in category:
            return 1.0 if "slam" in source else 0.0
        if "hushåll" in category:
            return 0.5 if "avfall" in source else 0.0
        return 0.0

    def _unit_score(self, feature: TaxKnowledgeFeature, standard_combined: str) -> float:
        unit_type = self.normalizer.normalize(feature.unit_type)
        if not unit_type:
            return 0.0
        if unit_type == "vikt" and ("vikg" in standard_combined or "kg" in standard_combined or "kilogram" in standard_combined):
            return 1.0
        if unit_type == "volym" and ("volm" in standard_combined or "m3" in standard_combined or "m³" in standard_combined):
            return 1.0
        if unit_type == "styck" and ("styck" in standard_combined or "st" in standard_combined):
            return 1.0
        if unit_type == "tillfälle" and ("tillfälle" in standard_combined or "gang" in standard_combined or "gång" in standard_combined):
            return 1.0
        return 0.0
