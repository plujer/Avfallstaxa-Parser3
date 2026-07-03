"""Missing/invalid tax row detection."""

from __future__ import annotations

from parser3.models import TaxRow


class MissingTaxDetector:
    def find_invalid_rows(self, rows: list[TaxRow]) -> list[str]:
        invalid: list[str] = []
        for idx, row in enumerate(rows, start=1):
            if not row.name.strip():
                invalid.append(f"Row {idx}: missing name")
            if row.export and not row.section.strip():
                invalid.append(f"Row {idx}: missing section for {row.name}")
        return invalid
