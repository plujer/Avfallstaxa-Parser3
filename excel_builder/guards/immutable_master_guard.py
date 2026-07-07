"""Runtime guards for immutable master files and protected workbook areas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass(frozen=True)
class FileFingerprint:
    path: Path
    sha256: str
    size_bytes: int
    mtime_ns: int


class ImmutableMasterViolation(RuntimeError):
    """Raised when code attempts to overwrite or alter a master source."""


class ImmutableMasterGuard:
    """Protect master files by path and fingerprint.

    The guard is intentionally simple: master files may be read and copied, but an
    output path may never resolve to a protected master path. Fingerprints can be
    captured before a run and verified after the run.
    """

    def __init__(self, protected_paths: list[str | Path]):
        self.protected_paths = tuple(Path(p).resolve() for p in protected_paths if str(p))

    def assert_output_allowed(self, output_path: str | Path) -> None:
        output = Path(output_path).resolve()
        if output in self.protected_paths:
            raise ImmutableMasterViolation(f"Output får inte vara masterfil: {output}")

    def fingerprint(self, path: str | Path) -> FileFingerprint:
        p = Path(path).resolve()
        return FileFingerprint(
            path=p,
            sha256=self._sha256(p),
            size_bytes=p.stat().st_size,
            mtime_ns=p.stat().st_mtime_ns,
        )

    def verify_unchanged(self, before: FileFingerprint) -> None:
        after = self.fingerprint(before.path)
        if before.sha256 != after.sha256 or before.size_bytes != after.size_bytes:
            raise ImmutableMasterViolation(f"Masterfil ändrades under körning: {before.path}")

    def assert_taxepunkter_write_allowed(self, column_index: int) -> None:
        if column_index <= 5:
            raise ImmutableMasterViolation("Taxepunkter kolumn A:E får inte skrivas automatiskt.")

    def assert_sheet_write_allowed(self, sheet_name: str, column_index: int | None = None) -> None:
        if sheet_name == "Taxa_från_edp":
            raise ImmutableMasterViolation("Taxa_från_edp är facit och får aldrig skrivas automatiskt.")
        if sheet_name == "Taxepunkter" and column_index is not None:
            self.assert_taxepunkter_write_allowed(column_index)

    def _sha256(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
