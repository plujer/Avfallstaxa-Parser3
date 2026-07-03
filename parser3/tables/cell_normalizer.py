"""Normalize table cell text."""

from __future__ import annotations

import re


class CellNormalizer:
    def normalize(self, value: str | None) -> str:
        text = (value or "").replace("\xa0", " ")
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def normalize_row(self, row: list[str]) -> list[str]:
        return [self.normalize(cell) for cell in row]

    def is_empty_row(self, row: list[str]) -> bool:
        return not any(self.normalize(cell) for cell in row)
