"""Run parser acceptance checks against manually verified facit."""

from __future__ import annotations

from parser3.acceptance.acceptance_models import (
    AcceptanceExpectation,
    AcceptanceResult,
    SectionAcceptanceResult,
)
from parser3.acceptance.name_normalizer import NameNormalizer
from parser3.models import TaxRow


class AcceptanceRunner:
    def __init__(self) -> None:
        self.normalizer = NameNormalizer()

    def run(self, rows: list[TaxRow], expectations: list[AcceptanceExpectation]) -> AcceptanceResult:
        result = AcceptanceResult()

        for expectation in expectations:
            section_rows = [
                row for row in rows
                if row.export and self._norm_section(row.section) == self._norm_section(expectation.section)
            ]

            names = [self.normalizer.normalize(row.name) for row in section_rows]

            missing_required = [
                name for name in expectation.required_names
                if self.normalizer.normalize(name) not in names
            ]

            wrongly_exported_ignored = [
                name for name in expectation.ignored_names
                if self.normalizer.normalize(name) in names
            ]

            actual_count = len(section_rows)
            passed = (
                actual_count == expectation.expected_count
                and not missing_required
                and not wrongly_exported_ignored
            )

            result.sections.append(
                SectionAcceptanceResult(
                    section=expectation.section,
                    expected_count=expectation.expected_count,
                    actual_count=actual_count,
                    passed=passed,
                    missing_required=missing_required,
                    wrongly_exported_ignored=wrongly_exported_ignored,
                )
            )

        return result

    def _norm_section(self, value: str) -> str:
        return " ".join((value or "").replace("\xa0", " ").strip().lower().split())
