"""Duplicate detection for tax rows."""

from __future__ import annotations

from collections import Counter
from parser3.models import TaxRow


class DuplicateDetector:
    def find_duplicates(self, rows: list[TaxRow]) -> list[str]:
        keys = [
            (row.section, row.group, row.name, row.variant, row.unit)
            for row in rows
            if row.export
        ]
        counts = Counter(keys)
        return [
            " | ".join(str(part) for part in key if part)
            for key, count in counts.items()
            if count > 1
        ]
