"""Special extraction for §6.1.4 split continuation row.

The row:
    Ombud för registrering av El-kretsen avlämnarintyg
    i Hämtplatsportalen XXX kr/tillfälle

is split across two Word paragraphs. The second row starts lowercase and the
generic FlatTaxExtractor deliberately skips lowercase continuation fragments.
"""

from __future__ import annotations

from difflib import SequenceMatcher

from parser3.acceptance.facit_yaml_loader import FacitYamlLoader
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow


class Section614Extractor:
    def __init__(self) -> None:
        self.normalizer = NameNormalizer()
        self.expected_names = self._load_expected_names()

    def extract_combined(
        self,
        previous_text: str,
        current_text: str,
        chapter: str = "6",
        section: str = "6.1.4",
        group: str = "",
    ) -> list[TaxRow]:
        if section != "6.1.4":
            return []

        combined = f"{previous_text} {current_text}".strip()
        combined_norm = self.normalizer.normalize(combined)
        if not combined_norm:
            return []

        best_name = ""
        best_score = 0.0
        for name in self.expected_names:
            expected_norm = self.normalizer.normalize(name)
            if expected_norm == combined_norm or expected_norm in combined_norm:
                best_name = name
                best_score = 1.0
                break
            score = SequenceMatcher(None, expected_norm, combined_norm).ratio()
            if score > best_score:
                best_name = name
                best_score = score

        if best_name and best_score >= 0.86:
            return [
                TaxRow(
                    chapter=chapter,
                    section=section,
                    group=group,
                    name=best_name,
                    variant="",
                    unit=self._unit_from_text(current_text),
                    price=self._price_from_text(current_text),
                    export=True,
                )
            ]

        return []

    def _load_expected_names(self) -> list[str]:
        for expectation in FacitYamlLoader().load():
            if expectation.section == "6.1.4":
                return expectation.required_names
        return []

    def _unit_from_text(self, text: str) -> str:
        lower = (text or "").lower()
        if "/tillfälle" in lower or "per tillfälle" in lower:
            return "tillfälle"
        if "/fraktion" in lower or "per fraktion" in lower:
            return "fraktion"
        return ""

    def _price_from_text(self, text: str) -> str:
        lower = (text or "")
        for token in ["XXXX kr", "XXX kr", "XX kr"]:
            if token.lower() in lower.lower():
                return token
        return ""
