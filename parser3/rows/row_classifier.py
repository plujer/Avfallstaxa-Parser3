"""Classify rows into tax/header/reference/info/empty."""

from __future__ import annotations

from dataclasses import dataclass

from parser3.rows.info_detector import InfoDetector
from parser3.rows.reference_detector import ReferenceDetector
from parser3.rows.tax_row_detector import TaxRowDetector
from parser3.utils.constants import (
    ROW_TYPE_EMPTY,
    ROW_TYPE_HEADER,
    ROW_TYPE_INFO,
    ROW_TYPE_REFERENCE,
    ROW_TYPE_TAX,
)


@dataclass
class ClassifiedRow:
    row_type: str
    text: str
    cells: list[str]


class RowClassifier:
    HEADER_WORDS = ["pris", "enhet", "ewc", "un-nr", "avgift", "typ av"]

    def __init__(self) -> None:
        self.reference_detector = ReferenceDetector()
        self.info_detector = InfoDetector()
        self.tax_detector = TaxRowDetector()

    def classify(self, cells: list[str]) -> ClassifiedRow:
        text = " ".join(c for c in cells if c).strip()
        lower = text.lower()

        if not text:
            return ClassifiedRow(ROW_TYPE_EMPTY, text, cells)

        if self.reference_detector.is_reference(text):
            return ClassifiedRow(ROW_TYPE_REFERENCE, text, cells)

        header_hits = sum(1 for word in self.HEADER_WORDS if word in lower)
        if header_hits >= 2 and "kr" not in lower:
            return ClassifiedRow(ROW_TYPE_HEADER, text, cells)

        if self.tax_detector.is_tax_candidate(text, cells):
            return ClassifiedRow(ROW_TYPE_TAX, text, cells)

        if self.info_detector.is_info(text):
            return ClassifiedRow(ROW_TYPE_INFO, text, cells)

        return ClassifiedRow(ROW_TYPE_INFO, text, cells)
