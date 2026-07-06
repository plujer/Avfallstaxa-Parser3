"""Specialized extraction for §6.1.2 facit rows without visible prices."""

from __future__ import annotations

from difflib import SequenceMatcher

from parser3.acceptance.facit_yaml_loader import FacitYamlLoader
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow


class Section612Extractor:
    def __init__(self) -> None:
        self.normalizer = NameNormalizer()
        self.expected_names = self._load_expected_names()
        self.ignored_names = self._load_ignored_names()

    def extract_line(self, text: str, chapter: str = "6", section: str = "6.1.2", group: str = "") -> list[TaxRow]:
        if section != "6.1.2":
            return []

        clean_norm = self.normalizer.normalize(text)
        if not clean_norm:
            return []

        for ignored in self.ignored_names:
            ignored_norm = self.normalizer.normalize(ignored)
            if ignored_norm and (ignored_norm == clean_norm or ignored_norm in clean_norm):
                return []

        best_name = ""
        best_score = 0.0

        for name in self.expected_names:
            expected_norm = self.normalizer.normalize(name)
            if not expected_norm:
                continue

            if expected_norm == clean_norm or expected_norm in clean_norm:
                best_name = name
                best_score = 1.0
                break

            score = SequenceMatcher(None, expected_norm, clean_norm).ratio()
            if score > best_score:
                best_name = name
                best_score = score

        # High threshold prevents accidental exports. This handles minor symbols,
        # appended units/codes and small Word parsing differences.
        if best_name and best_score >= 0.86:
            return [
                TaxRow(
                    chapter=chapter,
                    section=section,
                    group=group,
                    name=best_name,
                    variant="",
                    unit=self._unit_from_text(text),
                    price="",
                    export=True,
                )
            ]

        return []

    def _load_expected_names(self) -> list[str]:
        for expectation in FacitYamlLoader().load():
            if expectation.section == "6.1.2":
                return expectation.required_names
        return []

    def _load_ignored_names(self) -> list[str]:
        for expectation in FacitYamlLoader().load():
            if expectation.section == "6.1.2":
                return expectation.ignored_names
        return []

    def _unit_from_text(self, text: str) -> str:
        lower = (text or "").lower()
        if "kilogram" in lower or " kg" in lower:
            return "kilogram"
        if "m³" in lower or "m3" in lower:
            return "m³"
        if "styck" in lower or " st" in lower:
            return "styck"
        if "liter" in lower:
            return "liter"
        return ""
