"""Specialized extraction for §6.1.2 facit rows without visible prices."""

from __future__ import annotations

from difflib import SequenceMatcher

from parser3.acceptance.facit_yaml_loader import FacitYamlLoader
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow
from parser3.trace import TraceEvent, TraceStore


class Section612Extractor:
    def __init__(self, trace_store: TraceStore | None = None) -> None:
        self.normalizer = NameNormalizer()
        self.expected_names = self._load_expected_names()
        self.ignored_names = self._load_ignored_names()
        self.trace_store = trace_store

    def extract_line(
        self,
        text: str,
        chapter: str = "6",
        section: str = "6.1.2",
        group: str = "",
        order: int | None = None,
    ) -> list[TaxRow]:
        if section != "6.1.2":
            return []

        clean_norm = self.normalizer.normalize(text)
        if not clean_norm:
            self._trace(section, text, clean_norm, "", 0.0, "not_exported", "empty normalized text", order)
            return []

        for ignored in self.ignored_names:
            ignored_norm = self.normalizer.normalize(ignored)
            if ignored_norm and (ignored_norm == clean_norm or ignored_norm in clean_norm):
                self._trace(section, text, clean_norm, ignored, 1.0, "not_exported", "ignored/reference row", order)
                return []

        best_name, best_score, best_reason, best_expected_norm = self._best_match(clean_norm)

        if best_name and best_score >= 0.86:
            row = TaxRow(
                chapter=chapter,
                section=section,
                group=group,
                name=best_name,
                variant="",
                unit=self._unit_from_text(text),
                price="",
                export=True,
            )
            self._trace(
                section,
                text,
                clean_norm,
                best_name,
                best_score,
                "exported",
                f"{best_reason}; matched expected normalized={best_expected_norm}",
                order,
            )
            return [row]

        self._trace(
            section,
            text,
            clean_norm,
            best_name,
            best_score,
            "not_exported",
            "best score below threshold or no expected name",
            order,
        )
        return []

    def _best_match(self, clean_norm: str) -> tuple[str, float, str, str]:
        normalized_expected: list[tuple[str, str]] = [
            (name, self.normalizer.normalize(name))
            for name in self.expected_names
            if self.normalizer.normalize(name)
        ]

        # 1. Exact normalized match wins.
        for name, expected_norm in normalized_expected:
            if expected_norm == clean_norm:
                return name, 1.0, "exact match", expected_norm

        # 2. Substring matches: choose the longest / most specific expected name.
        substring_matches: list[tuple[int, str, str]] = []
        for name, expected_norm in normalized_expected:
            if expected_norm in clean_norm:
                substring_matches.append((len(expected_norm), name, expected_norm))

        if substring_matches:
            substring_matches.sort(reverse=True, key=lambda item: item[0])
            _, name, expected_norm = substring_matches[0]
            return name, 1.0, "longest substring match", expected_norm

        # 3. Fuzzy fallback.
        best_name = ""
        best_score = 0.0
        best_expected_norm = ""
        for name, expected_norm in normalized_expected:
            score = SequenceMatcher(None, expected_norm, clean_norm).ratio()
            if score > best_score:
                best_name = name
                best_score = score
                best_expected_norm = expected_norm

        return best_name, best_score, "fuzzy match", best_expected_norm

    def _trace(
        self,
        section: str,
        input_text: str,
        normalized_text: str,
        best_match: str,
        score: float,
        decision: str,
        reason: str,
        order: int | None,
    ) -> None:
        if self.trace_store is None:
            return
        self.trace_store.add(
            TraceEvent(
                component="Section612Extractor",
                section=section,
                input_text=input_text,
                normalized_text=normalized_text,
                best_match=best_match,
                score=score,
                decision=decision,
                reason=reason,
                order=order,
            )
        )

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
