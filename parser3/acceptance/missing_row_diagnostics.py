"""Deep diagnostics for missing acceptance rows.

This tool helps answer:
- Did WordReader read the expected text?
- Did SemanticParser classify it as INFO/REFERENCE/TAX_ROW?
- What normalized text was compared?
- Is the row split across several semantic rows?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from parser3.acceptance.facit_yaml_loader import FacitYamlLoader
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow
from parser3.semantic import SemanticRow


@dataclass
class MissingRowDiagnostic:
    section: str
    expected_name: str
    normalized_expected: str
    exact_semantic_hits: list[str] = field(default_factory=list)
    fuzzy_semantic_hits: list[str] = field(default_factory=list)
    nearby_semantic_rows: list[str] = field(default_factory=list)
    exported_similar_rows: list[str] = field(default_factory=list)


@dataclass
class MissingDiagnosticsResult:
    diagnostics: list[MissingRowDiagnostic] = field(default_factory=list)


class MissingRowDiagnostics:
    def __init__(self) -> None:
        self.normalizer = NameNormalizer()

    def run(self, tax_rows: list[TaxRow], semantic_rows: list[SemanticRow]) -> MissingDiagnosticsResult:
        result = MissingDiagnosticsResult()
        expectations = FacitYamlLoader().load()

        for expectation in expectations:
            if not expectation.required_names:
                continue

            exported_norm = {
                self.normalizer.normalize(row.name)
                for row in tax_rows
                if row.export and self._section(row.section) == self._section(expectation.section)
            }

            for expected_name in expectation.required_names:
                expected_norm = self.normalizer.normalize(expected_name)
                if expected_norm in exported_norm:
                    continue

                diagnostic = MissingRowDiagnostic(
                    section=expectation.section,
                    expected_name=expected_name,
                    normalized_expected=expected_norm,
                )

                section_semantic = [
                    row for row in semantic_rows
                    if self._section(row.section) == self._section(expectation.section)
                ]

                for row in section_semantic:
                    text_norm = self.normalizer.normalize(row.text)
                    line = self._format_semantic(row, text_norm)
                    if expected_norm and expected_norm in text_norm:
                        diagnostic.exact_semantic_hits.append(line)

                diagnostic.fuzzy_semantic_hits = self._fuzzy_semantic(expected_norm, section_semantic)
                diagnostic.nearby_semantic_rows = self._nearby_rows(expected_norm, section_semantic)
                diagnostic.exported_similar_rows = self._fuzzy_exported(expected_norm, tax_rows, expectation.section)

                result.diagnostics.append(diagnostic)

        return result

    def _fuzzy_semantic(self, expected_norm: str, rows: list[SemanticRow]) -> list[str]:
        scored: list[tuple[float, str]] = []
        for row in rows:
            text_norm = self.normalizer.normalize(row.text)
            score = SequenceMatcher(None, expected_norm, text_norm).ratio()
            if score >= 0.35:
                scored.append((score, self._format_semantic(row, text_norm, score)))
        scored.sort(reverse=True, key=lambda item: item[0])
        return [line for _, line in scored[:10]]

    def _nearby_rows(self, expected_norm: str, rows: list[SemanticRow]) -> list[str]:
        # A row may be split. Look for rows sharing at least two meaningful words.
        words = [w for w in expected_norm.replace(",", " ").replace("-", " ").split() if len(w) >= 4]
        found: list[str] = []
        for row in rows:
            text_norm = self.normalizer.normalize(row.text)
            hits = sum(1 for word in words if word in text_norm)
            if hits >= 2:
                found.append(self._format_semantic(row, text_norm))
        return found[:20]

    def _fuzzy_exported(self, expected_norm: str, rows: list[TaxRow], section: str) -> list[str]:
        scored: list[tuple[float, str]] = []
        for row in rows:
            if self._section(row.section) != self._section(section):
                continue
            name_norm = self.normalizer.normalize(row.name)
            score = SequenceMatcher(None, expected_norm, name_norm).ratio()
            if score >= 0.35:
                scored.append((score, f"{score:.3f} | {row.name} | unit={row.unit} | price={row.price}"))
        scored.sort(reverse=True, key=lambda item: item[0])
        return [line for _, line in scored[:10]]

    def _format_semantic(self, row: SemanticRow, text_norm: str, score: float | None = None) -> str:
        prefix = f"{score:.3f} | " if score is not None else ""
        return (
            f"{prefix}order={row.order} | type={row.row_type} | reason={row.reason} | "
            f"text={row.text} | normalized={text_norm}"
        )

    def _section(self, value: str) -> str:
        return " ".join((value or "").strip().lower().split())
