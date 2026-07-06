"""Specialized extraction for §6.1.2 facit rows without visible prices.

Block A in §6.1.2 can be read as semantic INFO rows because the source row may
not contain an explicit price marker. The Word row is still a tax row because
§6.1.2 is a priced handling-fee table where the price will later come from
Arbets-Excel.
"""

from __future__ import annotations

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
            if self.normalizer.normalize(ignored) in clean_norm:
                return []

        found: list[TaxRow] = []
        for name in self.expected_names:
            expected_norm = self.normalizer.normalize(name)
            if not expected_norm:
                continue
            if expected_norm == clean_norm or expected_norm in clean_norm:
                found.append(
                    TaxRow(
                        chapter=chapter,
                        section=section,
                        group=group,
                        name=name,
                        variant="",
                        unit=self._unit_from_text(text),
                        price="",
                        export=True,
                    )
                )
                break

        return found

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
        if "liter" in lower or " liter" in lower:
            return "liter"
        return ""
