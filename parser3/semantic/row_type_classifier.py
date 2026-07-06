from parser3.rows import RowClassifier
from parser3.rules import ReferenceRuleEngine
from parser3.utils.constants import ROW_TYPE_EMPTY, ROW_TYPE_GROUP, ROW_TYPE_HEADER, ROW_TYPE_INFO, ROW_TYPE_REFERENCE, ROW_TYPE_TAX

class RowTypeClassifier:
    GROUP_PHRASES = ["tillägg för farligt avfall", "tillägg för el-avfall", "övriga avgifter", "tillägg"]
    HEADER_PHRASES = ["typ av avfall", "ewc kod", "un-nr", "enhet", "pris", "avgift per"]

    def __init__(self) -> None:
        self.low_level = RowClassifier()
        self.reference_rules = ReferenceRuleEngine()

    def classify(self, cells: list[str]) -> tuple[str, str]:
        text = " ".join(c for c in cells if c).strip()
        lower = text.lower()
        if not text:
            return ROW_TYPE_EMPTY, "empty"
        if self.reference_rules.is_reference(text):
            return ROW_TYPE_REFERENCE, "reference rule"
        if any(phrase in lower for phrase in self.GROUP_PHRASES) and "kr" not in lower:
            return ROW_TYPE_GROUP, "group phrase"
        if sum(1 for phrase in self.HEADER_PHRASES if phrase in lower) >= 2:
            return ROW_TYPE_HEADER, "header phrase"
        classified = self.low_level.classify(cells)
        if classified.row_type == ROW_TYPE_TAX:
            return ROW_TYPE_TAX, "low-level tax candidate"
        if classified.row_type == ROW_TYPE_REFERENCE:
            return ROW_TYPE_REFERENCE, "low-level reference"
        if classified.row_type == ROW_TYPE_HEADER:
            return ROW_TYPE_HEADER, "low-level header"
        return ROW_TYPE_INFO, "default info"
