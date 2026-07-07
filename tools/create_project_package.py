from __future__ import annotations

import json
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "output",
    "rapportzip",
    "project_packages",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
}

EXCLUDE_FILES = {
    "Project_For_ChatGPT.zip",
    "PROJECT_PACKAGE_MANIFEST.txt",
    "PROJECT_INFO_FOR_CHATGPT.txt",
}


def is_excluded(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    parts = set(rel.parts)

    if parts & EXCLUDE_DIRS:
        return True

    if path.name in EXCLUDE_FILES:
        return True

    if path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True

    return False


def read_version(root: Path) -> str:
    version_file = root / "version.json"
    if not version_file.exists():
        return "unknown"

    try:
        data = json.loads(version_file.read_text(encoding="utf-8"))
        return str(data.get("version") or data.get("project_version") or "unknown")
    except Exception:
        return "unknown"


def create_package(root: Path) -> Path:
    output_dir = root / "project_packages"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_zip = output_dir / "Project_For_ChatGPT.zip"
    if output_zip.exists():
        output_zip.unlink()

    manifest_lines: list[str] = []
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if is_excluded(path, root):
            continue
        files.append(path)

    info_text = "\n".join(
        [
            "Excel Builder Project Package",
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Root: {root}",
            f"Version: {read_version(root)}",
            "",
            "Excluded directories:",
            *[f"- {d}" for d in sorted(EXCLUDE_DIRS)],
            "",
            "Excluded extensions:",
            *[f"- {e}" for e in sorted(EXCLUDE_EXTENSIONS)],
            "",
        ]
    )

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("PROJECT_INFO_FOR_CHATGPT.txt", info_text)

        for file_path in sorted(files):
            arcname = file_path.relative_to(root).as_posix()
            zf.write(file_path, arcname)
            manifest_lines.append(arcname)

        manifest_text = "\n".join(
            [
                "Project_For_ChatGPT manifest",
                f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"File count: {len(manifest_lines)}",
                "",
                *manifest_lines,
                "",
            ]
        )
        zf.writestr("PROJECT_PACKAGE_MANIFEST.txt", manifest_text)

    return output_zip

def main() -> int:
    root = Path.cwd().resolve()
    print()
    print("==========================================")
    print("Excel Builder - Project Package Tool")
    print("==========================================")
    print(f"Project root: {root}")

    try:
        output_zip = create_package(root)
    except Exception as exc:
        print()
        print("FAILED to create project package.")
        print(f"Error: {exc}")
        return 1

    print()
    print("Package created successfully:")
    print(output_zip)
    print()
    print("Send this file to ChatGPT:")
    print("project_packages/Project_For_ChatGPT.zip")
    print("==========================================")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
