"""Detect tables that continue across blocks/pages."""

from __future__ import annotations


class TableContinuationDetector:
    HEADER_TOKENS = {"typ av avfall", "ewc", "un-nr", "enhet", "pris"}

    def looks_like_same_table(self, previous_header: list[str], next_row: list[str]) -> bool:
        if not previous_header or not next_row:
            return False

        prev = " ".join(previous_header).lower()
        nxt = " ".join(next_row).lower()

        if any(token in nxt for token in self.HEADER_TOKENS):
            return True

        prev_cols = len(previous_header)
        next_cols = len(next_row)
        return abs(prev_cols - next_cols) <= 1

    def is_header_row(self, row: list[str]) -> bool:
        text = " ".join(row).lower()
        hits = sum(1 for token in self.HEADER_TOKENS if token in text)
        return hits >= 2
