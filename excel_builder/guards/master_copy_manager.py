"""Create working copies from immutable master files."""

from __future__ import annotations

from pathlib import Path
import shutil

from .immutable_master_guard import ImmutableMasterGuard


class MasterCopyManager:
    """Copies a master to an output path while verifying that the source is unchanged."""

    def __init__(self, protected_master_paths: list[str | Path]):
        self.guard = ImmutableMasterGuard(protected_master_paths)

    def create_copy(self, source: str | Path, output: str | Path) -> Path:
        source_path = Path(source)
        output_path = Path(output)
        self.guard.assert_output_allowed(output_path)
        before = self.guard.fingerprint(source_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, output_path)
        self.guard.verify_unchanged(before)
        return output_path
