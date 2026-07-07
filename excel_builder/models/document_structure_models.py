"""Models for document structure classification.

The Document Structure Engine separates real tax rows from headings, table
headers and notes before semantic matching/decisions. It is a non-destructive
layer: source parser rows are preserved and Taxa_från_edp is never modified.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from excel_builder.models.matching_models import ParserTaxRow


class DocumentRowType(StrEnum):
    SECTION = "SECTION"
    SUBSECTION = "SUBSECTION"
    TABLE_HEADER = "TABLE_HEADER"
    TABLE_ROW = "TABLE_ROW"
    TAX_NODE = "TAX_NODE"
    NOTE = "NOTE"


@dataclass
class DocumentStructureNode:
    row_index: int
    row_type: DocumentRowType
    parser_row: ParserTaxRow
    parent_index: int | None = None
    level: int = 0
    confidence: float = 0.0
    reason: str = ""


@dataclass
class DocumentStructureReport:
    nodes: list[DocumentStructureNode] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.nodes)

    def count(self, row_type: DocumentRowType | str) -> int:
        wanted = DocumentRowType(row_type)
        return sum(1 for node in self.nodes if node.row_type == wanted)

    @property
    def tax_nodes(self) -> list[DocumentStructureNode]:
        return [node for node in self.nodes if node.row_type == DocumentRowType.TAX_NODE]

    @property
    def tax_rows(self) -> list[ParserTaxRow]:
        return [node.parser_row for node in self.tax_nodes]
