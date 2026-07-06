"""Build a knowledge index from Tax Knowledge features and standard taxes.

The index groups likely comparable tax rows before matching. It does not make
final decisions and never writes EDP codes.
"""

from __future__ import annotations

import re

from excel_builder.matching import MatchNormalizer
from excel_builder.models import (
    KnowledgeIndex,
    KnowledgeIndexKey,
    StandardTaxCatalog,
    StandardTaxRow,
    TaxKnowledgeReport,
)


class KnowledgeIndexBuilder:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def build(self, knowledge_report: TaxKnowledgeReport, standard_catalog: StandardTaxCatalog) -> KnowledgeIndex:
        index = KnowledgeIndex()
        index.warnings.extend(knowledge_report.warnings)
        index.warnings.extend(standard_catalog.warnings)

        for feature in knowledge_report.features:
            key = self.key_from_feature(feature)
            entry = index.get_or_create(key)
            entry.feature_count += 1
            if len(entry.feature_examples) < 5:
                entry.feature_examples.append(feature)

        for standard_row in standard_catalog.rows:
            key = self.key_from_standard_row(standard_row)
            entry = index.get_or_create(key)
            entry.standard_rows.append(standard_row)

        return index

    def key_from_feature(self, feature) -> KnowledgeIndexKey:
        return KnowledgeIndexKey(
            category=feature.category,
            waste_type=feature.waste_type,
            unit_type=feature.unit_type,
            factor_hint=feature.factor_hint,
            container_volume_liter=feature.container_volume_liter,
        )

    def key_from_standard_row(self, row: StandardTaxRow) -> KnowledgeIndexKey:
        combined = self.normalizer.normalize(" ".join([
            row.source_sheet,
            row.strTaxekod,
            row.strTaxebenamning,
            row.strFaktor,
            row.strTaxedelAvser,
            row.strFormel,
        ]))
        tokens = self._tokens(combined)

        return KnowledgeIndexKey(
            category=self._category(row.source_sheet, combined, tokens),
            waste_type=self._waste_type(combined, tokens),
            unit_type=self._unit_type(combined, tokens),
            factor_hint=self._factor_hint(row.strFaktor, combined, tokens),
            container_volume_liter=self._container_volume(combined),
        )

    def candidate_entries_for_feature(self, index: KnowledgeIndex, feature) -> list:
        exact_key = self.key_from_feature(feature)
        candidates = []

        if exact_key in index.entries:
            candidates.append(index.entries[exact_key])

        for key, entry in index.entries.items():
            if key == exact_key:
                continue

            score = 0
            if key.category and key.category == feature.category:
                score += 1
            if key.waste_type and key.waste_type == feature.waste_type:
                score += 2
            if key.factor_hint and key.factor_hint == feature.factor_hint:
                score += 2
            if key.unit_type and key.unit_type == feature.unit_type:
                score += 1
            if key.container_volume_liter and key.container_volume_liter == feature.container_volume_liter:
                score += 2

            if score >= 3:
                candidates.append(entry)

        return candidates

    def _category(self, source_sheet: str, text: str, tokens: set[str]) -> str:
        source = self.normalizer.normalize(source_sheet)
        if "slam" in source or "slam" in tokens:
            return "Slam"
        if "avfall" in source:
            return "ÅVC/verksamhetsavfall"
        if "åvs" in source or "avs" in source:
            return "ÅVS"
        return ""

    def _waste_type(self, text: str, tokens: set[str]) -> str:
        rules = [
            ({"asbest"}, "Asbest"),
            ({"gips", "gipsskivor"}, "Gips"),
            ({"tryckimpregnerat"}, "Tryckimpregnerat trä"),
            ({"betong", "lättbetong"}, "Betong"),
            ({"tegel"}, "Tegel"),
            ({"metall"}, "Metall"),
            ({"plast"}, "Plast"),
            ({"batteri", "batterier"}, "Batterier"),
            ({"elavfall", "el-avfall"}, "Elavfall"),
            ({"slam", "slamtömning"}, "Slam"),
            ({"matavfall"}, "Matavfall"),
            ({"restavfall"}, "Restavfall"),
            ({"förpackning", "förpackningar", "forpackning", "forpackningar"}, "Förpackningar"),
        ]
        for needles, value in rules:
            if tokens.intersection(needles):
                return value
        if "trä" in tokens or "träavfall" in tokens or "virke" in tokens:
            return "Träavfall"
        if "olja" in tokens or "oljefilter" in tokens or "olje" in text:
            return "Oljeavfall"
        if "farligt" in tokens:
            return "Farligt avfall"
        return ""

    def _unit_type(self, text: str, tokens: set[str]) -> str:
        if "vikg" in tokens or "kg" in tokens or "kilogram" in tokens:
            return "Vikt"
        if "volm" in tokens or "m3" in tokens or "m³" in tokens or "kubikmeter" in tokens:
            return "Volym"
        if "styck" in tokens or "st" in tokens:
            return "Styck"
        if "liter" in tokens or re.search(r"\b\d+\s*l\b", text):
            return "Behållarvolym"
        if "tillfälle" in tokens or "gång" in tokens or "gang" in tokens:
            return "Tillfälle"
        return ""

    def _factor_hint(self, factor: str, text: str, tokens: set[str]) -> str:
        factor_norm = self.normalizer.normalize(factor)
        if factor_norm:
            return factor_norm.upper()
        unit_type = self._unit_type(text, tokens)
        if unit_type == "Vikt":
            return "VIKG"
        if unit_type == "Volym":
            return "VOLM"
        if unit_type == "Styck":
            return "ST"
        if unit_type == "Behållarvolym":
            return "VOLYM/BEHÅLLARE"
        if unit_type == "Tillfälle":
            return "TILLFÄLLE"
        return ""

    def _container_volume(self, text: str) -> str:
        match = re.search(r"\b(\d{2,4})\s*l\b", text)
        if match:
            return match.group(1)
        match = re.search(r"\b(\d{2,4})\s*liter\b", text)
        if match:
            return match.group(1)
        return ""

    def _tokens(self, text: str) -> set[str]:
        return {token for token in re.split(r"[^a-zåäö0-9-]+", text) if token}
