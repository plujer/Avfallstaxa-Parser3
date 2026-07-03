"""Validate extracted rows against golden master counts."""

from __future__ import annotations

from collections import Counter
from typing import Any

from parser3.models import TaxRow


class GoldenMasterValidator:
    def validate_counts(self, rows: list[TaxRow], golden_master: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        expected_sections = golden_master.get("sections", {}) or {}
        actual = Counter(row.section for row in rows if row.export)

        for section, spec in expected_sections.items():
            expected_count = int((spec or {}).get("tax_count", 0))
            actual_count = int(actual.get(section, 0))
            if expected_count != actual_count:
                errors.append(
                    f"Section {section}: expected {expected_count} tax rows, got {actual_count}"
                )

        return errors
