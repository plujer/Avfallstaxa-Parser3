"""Run parser acceptance checks against manually verified facit."""

from __future__ import annotations

from parser3.acceptance.acceptance_models import (
    AcceptanceExpectation,
    AcceptanceResult,
    SectionAcceptanceResult,
)
from parser3.models import TaxRow


class AcceptanceRunner:
    def run(self, rows: list[TaxRow], expectations: list[AcceptanceExpectation]) -> AcceptanceResult:
        result = AcceptanceResult()

        for expectation in expectations:
            section_rows = [
                row for row in rows
                if row.export and self._norm(row.section) == self._norm(expectation.section)
            ]

            names = [self._norm(row.name) for row in section_rows]

            missing_required = [
                name for name in expectation.required_names
                if self._norm(name) not in names
            ]

            wrongly_exported_ignored = [
                name for name in expectation.ignored_names
                if self._norm(name) in names
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

    def _norm(self, value: str) -> str:
        value = (value or "").replace("\xa0", " ").replace("–", "-").strip().lower()
        return " ".join(value.split())
