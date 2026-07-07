from __future__ import annotations

from pathlib import Path

from excel_builder.models.project_metadata_models import ProjectMetadata, ReleaseChecklistItem


class ReleaseChecklistBuilder:
    def build(self, metadata: ProjectMetadata, project_root: str | Path = ".") -> tuple[ReleaseChecklistItem, ...]:
        root = Path(project_root)
        expected = {
            "run_project.bat": root / "run_project.bat",
            "run_tests.bat": root / "run_tests.bat",
            "run_reports.bat": root / "run_reports.bat",
            "run_clean.bat": root / "run_clean.bat",
            "git_commit_block.bat": root / "git_commit_block.bat",
            "git_release_block.bat": root / "git_release_block.bat",
            "PROJECT_STATUS.md": root / "docs" / "PROJECT_STATUS.md",
            "CHANGELOG.md": root / "docs" / "CHANGELOG.md",
            "BLOCK_HISTORY.md": root / "docs" / "history" / "BLOCK_HISTORY.md",
        }
        items: list[ReleaseChecklistItem] = []
        for name, path in expected.items():
            items.append(ReleaseChecklistItem(name=name, passed=path.exists(), detail=str(path)))

        tag_ok = metadata.release_tag == f"{metadata.version}-block{metadata.block_id}"
        items.append(
            ReleaseChecklistItem(
                name="release_tag_format",
                passed=tag_ok,
                detail=f"{metadata.release_tag} (förväntat {metadata.version}-block{metadata.block_id})",
            )
        )
        items.append(
            ReleaseChecklistItem(
                name="metadata_status",
                passed=metadata.status in {"development", "verified", "release-ready"},
                detail=metadata.status,
            )
        )
        return tuple(items)
