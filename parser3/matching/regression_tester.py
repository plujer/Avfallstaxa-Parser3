"""Regression testing against golden master."""

from __future__ import annotations

from collections import Counter

from parser3.models import TaxRow


class RegressionTester:
    def compare_counts(self, rows: list[TaxRow], golden_master: dict) -> list[str]:
        errors: list[str] = []
        actual = Counter(row.section for row in rows if row.export)

        for section, spec in (golden_master.get("sections", {}) or {}).items():
            expected = int((spec or {}).get("tax_count", 0))
            got = int(actual.get(section, 0))
            if expected != got:
                errors.append(f"{section}: expected {expected}, got {got}")

        return errors
