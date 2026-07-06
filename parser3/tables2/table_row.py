"""Structured table row models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TableCell:
    index: int
    text: str


@dataclass
class TableRow:
    cells: list[TableCell] = field(default_factory=list)
    raw_cells: list[str] = field(default_factory=list)
    source_order: int = 0

    @property
    def text(self) -> str:
        return " ".join(cell.text for cell in self.cells if cell.text).strip()

    def cell_text(self, index: int) -> str:
        if index < 0 or index >= len(self.raw_cells):
            return ""
        return self.raw_cells[index].strip()

    @property
    def first_non_price_cell(self) -> str:
        for cell in self.cells:
            if cell.text and "kr" not in cell.text.lower():
                return cell.text
        return self.cells[0].text if self.cells else ""
