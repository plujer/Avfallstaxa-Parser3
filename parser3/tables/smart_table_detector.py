"""Smart detector for native and visual tables."""

from __future__ import annotations

from dataclasses import dataclass, field

from parser3.document import DocumentBlock
from parser3.tables.native_word_table_reader import NativeWordTableReader
from parser3.tables.visual_table_detector import VisualTableDetector


@dataclass
class DetectedTable:
    source: str
    start_order: int
    rows: list[list[str]] = field(default_factory=list)


class SmartTableDetector:
    def __init__(self) -> None:
        self.native_reader = NativeWordTableReader()
        self.visual_detector = VisualTableDetector()

    def detect(self, blocks: list[DocumentBlock]) -> list[DetectedTable]:
        tables: list[DetectedTable] = []

        for block in blocks:
            if block.kind == "table":
                rows = self.native_reader.read(block)
                if rows:
                    tables.append(DetectedTable(source="native", start_order=block.order, rows=rows))

        for run in self.visual_detector.collect_runs(blocks):
            rows = [[b.text] for b in run]
            tables.append(DetectedTable(source="visual", start_order=run[0].order, rows=rows))

        return sorted(tables, key=lambda t: t.start_order)
