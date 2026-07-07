"""Protected workbook range rules for immutable master templates."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .immutable_master_guard import ImmutableMasterViolation


@dataclass(frozen=True)
class ProtectedRangeRule:
    sheet_name: str
    protected_columns: str
    message: str


def column_letter_to_index(value: str) -> int:
    text = value.strip().upper()
    if not re.fullmatch(r"[A-Z]+", text):
        raise ValueError(f"Invalid Excel column: {value!r}")
    idx = 0
    for char in text:
        idx = idx * 26 + (ord(char) - ord("A") + 1)
    return idx


def column_in_rule(column_index: int, protected_columns: str) -> bool:
    rule = (protected_columns or "").strip().upper()
    if not rule:
        return False
    if rule == "ALL":
        return True

    for part in rule.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            start, end = [p.strip() for p in part.split(":", 1)]
            if column_letter_to_index(start) <= column_index <= column_letter_to_index(end):
                return True
        else:
            if column_letter_to_index(part) == column_index:
                return True
    return False


class ProtectedRangeGuard:
    """Blocks writes to protected cells/columns based on sheet rules."""

    def __init__(self, rules: list[ProtectedRangeRule] | tuple[ProtectedRangeRule, ...]):
        self.rules = tuple(rules)

    def assert_write_allowed(self, sheet_name: str, column_index: int | None = None) -> None:
        for rule in self.rules:
            if rule.sheet_name != sheet_name:
                continue
            if rule.protected_columns.strip().upper() == "ALL":
                raise ImmutableMasterViolation(rule.message)
            if column_index is not None and column_in_rule(column_index, rule.protected_columns):
                raise ImmutableMasterViolation(rule.message)
