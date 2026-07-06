"""Debug missing/extra acceptance rows section by section."""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from parser3.acceptance.facit_catalog import FacitCatalog
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow
from parser3.semantic import SemanticRow


@dataclass
class SectionDebugResult:
    section: str
    expected_names: list[str] = field(default_factory=list)
    exported_names: list[str] = field(default_factory=list)
    missing_names: list[str] = field(default_factory=list)
    extra_names: list[str] = field(default_factory=list)
    possible_matches: dict[str, list[str]] = field(default_factory=dict)
    non_tax_candidates: list[str] = field(default_factory=list)


@dataclass
class AcceptanceDebugResult:
    sections: list[SectionDebugResult] = field(default_factory=list)


class AcceptanceDebugger:
    def __init__(self) -> None:
        self.catalog = FacitCatalog()
        self.normalizer = NameNormalizer()

    def debug(self, rows: list[TaxRow], semantic_rows: list[SemanticRow]) -> AcceptanceDebugResult:
        result = AcceptanceDebugResult()
        catalog = self.catalog.rows_by_section()

        for section, expected_names in catalog.items():
            exported = [row.name for row in rows if row.export and self._norm_section(row.section) == self._norm_section(section)]
            exported_norm = {self.normalizer.normalize(name): name for name in exported}
            expected_norm = {self.normalizer.normalize(name): name for name in expected_names}

            missing = [
                original for norm, original in expected_norm.items()
                if norm not in exported_norm
            ]

            extra = [
                original for norm, original in exported_norm.items()
                if norm not in expected_norm
            ]

            possible: dict[str, list[str]] = {}
            for missing_name in missing:
                suggestions = self._closest(missing_name, exported)
                if suggestions:
                    possible[missing_name] = suggestions

            non_tax_candidates = self._semantic_candidates(section, missing, semantic_rows)

            result.sections.append(
                SectionDebugResult(
                    section=section,
                    expected_names=expected_names,
                    exported_names=exported,
                    missing_names=missing,
                    extra_names=extra,
                    possible_matches=possible,
                    non_tax_candidates=non_tax_candidates,
                )
            )

        return result

    def _closest(self, name: str, candidates: list[str]) -> list[str]:
        scored = []
        name_norm = self.normalizer.normalize(name)
        for candidate in candidates:
            score = SequenceMatcher(None, name_norm, self.normalizer.normalize(candidate)).ratio()
            if score >= 0.55:
                scored.append((score, candidate))
        scored.sort(reverse=True)
        return [candidate for _, candidate in scored[:5]]

    def _semantic_candidates(self, section: str, missing: list[str], semantic_rows: list[SemanticRow]) -> list[str]:
        found: list[str] = []
        missing_norm = [(name, self.normalizer.normalize(name)) for name in missing]

        for row in semantic_rows:
            if self._norm_section(row.section) != self._norm_section(section):
                continue
            text_norm = self.normalizer.normalize(row.text)
            for original, norm in missing_norm:
                if norm and (norm in text_norm or text_norm in norm):
                    found.append(f"{row.row_type} | {row.reason} | {row.text}")
                    break

        return found

    def _norm_section(self, value: str) -> str:
        return " ".join((value or "").replace("\xa0", " ").strip().lower().split())
