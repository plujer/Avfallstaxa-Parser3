"""Central guard for immutable master sources and protected workbook areas."""

from __future__ import annotations

from pathlib import Path

from excel_builder.config import MasterSourcesReader

from .immutable_master_guard import FileFingerprint, ImmutableMasterGuard, ImmutableMasterViolation
from .immutable_sheet_guard import ImmutableSheetGuard
from .protected_range_guard import ProtectedRangeGuard, ProtectedRangeRule
from .master_copy_manager import MasterCopyManager


class MasterGuard:
    """One access point for master-source safety rules.

    Rules enforced:
    - Word and Excel master files may be read and copied, never written/overwritten.
    - Taxa_från_edp is a fully immutable sheet.
    - Taxepunkter columns A:E are immutable template columns.
    - Any master edit requires a new versioned master file outside this guard.
    """

    def __init__(self, config_path: str | Path | None = None):
        self.sources = MasterSourcesReader().read(config_path)
        self.file_guard = ImmutableMasterGuard([self.sources.word_master, self.sources.excel_master])
        range_rules = []
        immutable_sheets = []
        for rule in self.sources.protected_sheets:
            if rule.protected_columns.upper() == "ALL":
                immutable_sheets.append(rule.sheet_name)
            range_rules.append(
                ProtectedRangeRule(
                    sheet_name=rule.sheet_name,
                    protected_columns=rule.protected_columns,
                    message=rule.rule or f"Skyddad skrivning blockerad i {rule.sheet_name}.",
                )
            )
        self.sheet_guard = ImmutableSheetGuard(tuple(immutable_sheets))
        self.range_guard = ProtectedRangeGuard(tuple(range_rules))
        self.copy_manager = MasterCopyManager([self.sources.word_master, self.sources.excel_master])

    def assert_output_path_allowed(self, output_path: str | Path) -> None:
        self.file_guard.assert_output_allowed(output_path)

    def assert_workbook_write_allowed(self, sheet_name: str, column_index: int | None = None) -> None:
        self.sheet_guard.assert_sheet_write_allowed(sheet_name)
        self.range_guard.assert_write_allowed(sheet_name, column_index)

    def fingerprint_masters(self) -> dict[str, FileFingerprint]:
        return {
            "word_master": self.file_guard.fingerprint(self.sources.word_master),
            "excel_master": self.file_guard.fingerprint(self.sources.excel_master),
        }

    def verify_masters_unchanged(self, fingerprints: dict[str, FileFingerprint]) -> None:
        for fingerprint in fingerprints.values():
            self.file_guard.verify_unchanged(fingerprint)

    def create_excel_working_copy(self, output_path: str | Path) -> Path:
        return self.copy_manager.create_copy(self.sources.excel_master, output_path)
