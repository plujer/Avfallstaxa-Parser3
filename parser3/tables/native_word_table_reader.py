"""Convert DocumentBlock table rows into normalized table rows."""

from __future__ import annotations

from parser3.document import DocumentBlock
from parser3.tables.cell_normalizer import CellNormalizer


class NativeWordTableReader:
    def __init__(self, normalizer: CellNormalizer | None = None) -> None:
        self.normalizer = normalizer or CellNormalizer()

    def read(self, block: DocumentBlock) -> list[list[str]]:
        if block.kind != "table":
            return []
        rows: list[list[str]] = []
        for row in block.rows:
            normalized = self.normalizer.normalize_row(row)
            if not self.normalizer.is_empty_row(normalized):
                rows.append(normalized)
        return rows
