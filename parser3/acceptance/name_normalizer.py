"""Name normalization for acceptance comparison.

This layer is only for comparing parser output with facit. It must not change the
source Word text or the generated Excel rows.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher


class NameNormalizer:
    ALIASES = {
        "förpackningar, tömde ej rengjorda": "förpackningar, tömda ej rengjorda",
        "gasol inkl tub": "gasol inkl. tub",
        "flourvätesyra": "fluorvätesyra",
        "surt oorganisk fast ämne": "surt oorganiskt fast ämne",
        "surt organisk fast ämne": "surt organiskt fast ämne",
        "rengöring/vaskmedel fast": "rengörings-/vaskmedel fast",
        "färg-,lack-, limburkar vattenbaserade": "färg-, lack-, limburkar vattenbaserade",
        "härdare metyl- etylketonperoxid": "härdare metyl-etylketonperoxid",
        "oljeavfall, fast osorterat emba": "oljeavfall, fast osorterat emballage",
        "wc stol": "wc-stol",
        "stubbar rötter för krossning": "stubbar/rötter för krossning",
    }

    UNIT_WORDS = {
        "kilogram", "kg", "liter", "l", "m³", "m3", "styck", "st", "ton", "container",
        "dygn", "vecka", "år", "tömning", "besök", "budning", "bunt", "säck",
    }

    def normalize(self, value: str) -> str:
        text = self._basic_clean(value)

        # Remove structured metadata before duplicate collapse. Word tables can
        # produce: NAME NAME EWC EWC UNIT UNIT.
        text_without_metadata = self._remove_metadata_tokens(text)
        text_without_metadata = self._remove_trailing_price(text_without_metadata)
        text_without_metadata = self._standardize_spacing(text_without_metadata)
        text_without_metadata = self._remove_trailing_units(text_without_metadata)
        text_without_metadata = self._collapse_repeated_sequence(text_without_metadata)

        text = self._standardize_spacing(text_without_metadata)
        text = self._remove_trailing_units(text)
        text = self._collapse_duplicate_halves(text)
        text = text.strip(" .;:")
        text = self.ALIASES.get(text, text)
        return text

    def _basic_clean(self, value: str) -> str:
        text = (value or "").replace("\xa0", " ")
        text = text.replace("–", "-").replace("—", "-")
        text = text.replace("×", "x").replace("*", "x")
        return text.lower().strip()

    def _standardize_spacing(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*/\s*", "/", text)
        text = re.sub(r"\s*-\s*", "-", text)
        text = re.sub(r"\s*x\s*", "x", text)
        text = text.replace("m3", "m³")
        text = text.replace(" inkl ", " inkl. ")
        text = re.sub(r"\binkl\.\.", "inkl.", text)
        return text.strip()

    def _remove_metadata_tokens(self, text: str) -> str:
        # Remove EWC codes and UN numbers that can be appended to table text.
        text = re.sub(r"\b\d{6}\*?\b", " ", text)
        text = re.sub(r"\bun[- ]?nr\b", " ", text)
        text = re.sub(r"\bewc(?: kod)?\b", " ", text)

        # Remove common UN numbers when they stand alone after a row.
        text = re.sub(r"\b\d{4}\b", " ", text)
        return text

    def _remove_trailing_price(self, text: str) -> str:
        return re.sub(r"(?i)\b(?:xx+|\d[\d\s]*,\d{2}|\d+)\s*kr\b", " ", text)

    def _remove_trailing_units(self, text: str) -> str:
        parts = text.split()
        while parts and parts[-1].strip(".,;:") in self.UNIT_WORDS:
            parts.pop()
        return " ".join(parts)

    def _collapse_duplicate_halves(self, text: str) -> str:
        parts = text.split()
        if len(parts) % 2 != 0 or not parts:
            return text
        half = len(parts) // 2
        if parts[:half] == parts[half:]:
            return " ".join(parts[:half])
        return text

    def _collapse_repeated_sequence(self, text: str) -> str:
        """Collapse repeated name sequences, even after metadata removal.

        Example:
        "skrymmande ... 20x20x80 skrymmande ... 20x20x80"
        becomes:
        "skrymmande ... 20x20x80"
        """
        text = text.strip()
        if not text:
            return text

        parts = text.split()
        n = len(parts)

        # Exact repeated prefix/suffix with possible short residue.
        for size in range(n // 2, 1, -1):
            first = parts[:size]
            second = parts[size:size * 2]
            if first == second:
                return " ".join(first + parts[size * 2:]).strip()

        # Fuzzy duplicate detection for rows where punctuation changed.
        best_size = 0
        best_score = 0.0
        for size in range(n // 2, 2, -1):
            first = " ".join(parts[:size])
            second = " ".join(parts[size:size * 2])
            score = SequenceMatcher(None, first, second).ratio()
            if score > best_score:
                best_score = score
                best_size = size

        if best_size and best_score >= 0.92:
            return " ".join(parts[:best_size] + parts[best_size * 2:]).strip()

        return text
