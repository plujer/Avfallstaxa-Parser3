"""Sheet-level immutability rules."""

from __future__ import annotations

from .immutable_master_guard import ImmutableMasterViolation


class ImmutableSheetGuard:
    """Blocks writes to whole immutable sheets."""

    def __init__(self, immutable_sheets: list[str] | tuple[str, ...]):
        self.immutable_sheets = frozenset(immutable_sheets)

    def assert_sheet_write_allowed(self, sheet_name: str) -> None:
        if sheet_name in self.immutable_sheets:
            raise ImmutableMasterViolation(
                f"Bladet {sheet_name!r} är immutable och får aldrig skrivas automatiskt."
            )
