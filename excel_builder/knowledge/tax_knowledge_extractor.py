"""Extract structured tax knowledge from parser rows.

This is the first step toward rule-based tax matching. It does not decide or
write EDP codes. It only classifies the Word/parser tax rows.
"""

from __future__ import annotations

import re

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ParserTaxRow, TaxKnowledgeFeature, TaxKnowledgeReport


class TaxKnowledgeExtractor:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def extract(self, parser_rows: list[ParserTaxRow]) -> TaxKnowledgeReport:
        report = TaxKnowledgeReport()

        for row in parser_rows:
            text = self.normalizer.normalize(" ".join([
                row.section,
                row.tax_point,
                row.variant,
                row.unit,
            ]))

            feature = TaxKnowledgeFeature(
                parser_row=row,
                section_group=self._section_group(row.section),
                category=self._category(row.section, text),
                waste_type=self._waste_type(text),
                unit_type=self._unit_type(row.unit, text),
                container_volume_liter=self._container_volume(text),
                factor_hint=self._factor_hint(row.unit, text),
                keywords=self._keywords(text),
            )

            feature.confidence = self._confidence(feature)
            feature.notes = self._notes(feature)
            report.features.append(feature)

        return report

    def _section_group(self, section: str) -> str:
        normalized = self.normalizer.normalize_section(section)
        parts = normalized.split(".")
        if len(parts) >= 2:
            return ".".join(parts[:2])
        return normalized

    def _category(self, section: str, text: str) -> str:
        section_norm = self.normalizer.normalize_section(section)

        if section_norm.startswith("6.1.2"):
            return "ÅVC/verksamhetsavfall"
        if section_norm.startswith("6.1"):
            return "Verksamhetsavfall"
        if section_norm.startswith("5"):
            return "Slam"
        if section_norm.startswith("4"):
            return "Tilläggstjänst"
        if section_norm.startswith("3"):
            return "Flerbostad/verksamhet"
        if section_norm.startswith("2"):
            return "Hushåll"
        if "återvinningscentral" in text or "åvc" in text:
            return "ÅVC/verksamhetsavfall"
        if "slam" in text or "slamtömning" in text:
            return "Slam"
        return "Okänd"

    def _waste_type(self, text: str) -> str:
        rules = [
            ("asbest", "Asbest"),
            ("gips", "Gips"),
            ("trä", "Träavfall"),
            ("tra", "Träavfall"),
            ("tryckimpregnerat", "Tryckimpregnerat trä"),
            ("betong", "Betong"),
            ("tegel", "Tegel"),
            ("metall", "Metall"),
            ("plast", "Plast"),
            ("farligt", "Farligt avfall"),
            ("olje", "Oljeavfall"),
            ("batteri", "Batterier"),
            ("elavfall", "Elavfall"),
            ("el-avfall", "Elavfall"),
            ("kyl", "Kyl/frys"),
            ("frys", "Kyl/frys"),
            ("slam", "Slam"),
            ("matavfall", "Matavfall"),
            ("restavfall", "Restavfall"),
            ("förpackning", "Förpackningar"),
            ("forpackning", "Förpackningar"),
        ]

        for needle, value in rules:
            if needle in text:
                return value
        return ""

    def _unit_type(self, unit: str, text: str) -> str:
        unit_norm = self.normalizer.normalize(unit)

        if unit_norm in {"kg", "kilogram"} or "kilogram" in text:
            return "Vikt"
        if unit_norm in {"ton"} or " ton" in f" {text}":
            return "Vikt"
        if unit_norm in {"m3", "m³", "kubikmeter"} or "m3" in text or "m³" in text:
            return "Volym"
        if unit_norm in {"st", "styck", "st."} or "styck" in text:
            return "Styck"
        if "liter" in text or re.search(r"\b\d+\s*l\b", text):
            return "Behållarvolym"
        if "gång" in text or "gang" in text or "tillfälle" in text:
            return "Tillfälle"
        return ""

    def _container_volume(self, text: str) -> str:
        match = re.search(r"\b(\d{2,4})\s*l\b", text)
        if match:
            return match.group(1)
        match = re.search(r"\b(\d{2,4})\s*liter\b", text)
        if match:
            return match.group(1)
        return ""

    def _factor_hint(self, unit: str, text: str) -> str:
        unit_type = self._unit_type(unit, text)
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

    def _keywords(self, text: str) -> list[str]:
        words = []
        for token in re.split(r"[^a-zåäö0-9]+", text):
            if len(token) < 3:
                continue
            if token in {"och", "med", "utan", "för", "fran", "från", "till", "per"}:
                continue
            words.append(token)
        return sorted(set(words))

    def _confidence(self, feature: TaxKnowledgeFeature) -> float:
        score = 0.0
        if feature.section_group:
            score += 0.20
        if feature.category and feature.category != "Okänd":
            score += 0.25
        if feature.waste_type:
            score += 0.25
        if feature.unit_type:
            score += 0.15
        if feature.factor_hint:
            score += 0.10
        if feature.keywords:
            score += 0.05
        return min(score, 1.0)

    def _notes(self, feature: TaxKnowledgeFeature) -> list[str]:
        notes: list[str] = []
        if not feature.category or feature.category == "Okänd":
            notes.append("Kategori okänd – regel kan behöva kompletteras.")
        if not feature.factor_hint:
            notes.append("Faktor kunde inte härledas från enhet/text.")
        if not feature.waste_type:
            notes.append("Avfallstyp kunde inte härledas.")
        return notes
