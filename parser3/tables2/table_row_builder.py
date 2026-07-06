"""Build structured table rows from raw cell lists."""

from __future__ import annotations

from parser3.tables.cell_normalizer import CellNormalizer
from parser3.tables2.table_row import TableCell, TableRow


class TableRowBuilder:
    def __init__(self) -> None:
        self.normalizer = CellNormalizer()

    def build(self, raw_cells: list[str], source_order: int = 0) -> TableRow:
        normalized = self.normalizer.normalize_row(raw_cells)
        return TableRow(
            cells=[TableCell(index=i, text=text) for i, text in enumerate(normalized)],
            raw_cells=normalized,
            source_order=source_order,
        )
