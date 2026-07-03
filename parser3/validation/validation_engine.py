"""Validation engine for Parser 3.0."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from parser3.models import TaxRow
from parser3.validation.duplicate_detector import DuplicateDetector
from parser3.validation.golden_master_loader import GoldenMasterLoader
from parser3.validation.golden_master_validator import GoldenMasterValidator
from parser3.validation.missing_tax_detector import MissingTaxDetector


@dataclass
class ValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ValidationEngine:
    def __init__(self) -> None:
        self.duplicate_detector = DuplicateDetector()
        self.missing_tax_detector = MissingTaxDetector()
        self.golden_loader = GoldenMasterLoader()
        self.golden_validator = GoldenMasterValidator()

    def validate(
        self,
        rows: list[TaxRow],
        golden_master_path: str | Path | None = None,
    ) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        duplicates = self.duplicate_detector.find_duplicates(rows)
        for duplicate in duplicates:
            warnings.append(f"Duplicate tax row: {duplicate}")

        errors.extend(self.missing_tax_detector.find_invalid_rows(rows))

        if golden_master_path:
            golden = self.golden_loader.load(golden_master_path)
            errors.extend(self.golden_validator.validate_counts(rows, golden))

        return ValidationResult(passed=not errors, errors=errors, warnings=warnings)
