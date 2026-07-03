"""Split tables into logical table sections."""

from __future__ import annotations

from parser3.tables.table_continuation_detector import TableContinuationDetector


class TableSplitter:
    def __init__(self, continuation_detector: TableContinuationDetector | None = None) -> None:
        self.continuation_detector = continuation_detector or TableContinuationDetector()

    def split_on_headers(self, rows: list[list[str]]) -> list[list[list[str]]]:
        sections: list[list[list[str]]] = []
        current: list[list[str]] = []

        for row in rows:
            if self.continuation_detector.is_header_row(row) and current:
                sections.append(current)
                current = [row]
            else:
                current.append(row)

        if current:
            sections.append(current)

        return sections
