from __future__ import annotations

import json
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
    "archive",
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
}

OUTPUT_DIR = "project_packages"
OUTPUT_NAME = "Project_For_ChatGPT.zip"
INFO_NAME = "PROJECT_INFO_FOR_CHATGPT.txt"
MANIFEST_NAME = "PROJECT_PACKAGE_MANIFEST.txt"


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
    output_dir = root / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    output_zip = output_dir / OUTPUT_NAME
    manifest_path = output_dir / MANIFEST_NAME
    info_path = output_dir / INFO_NAME

    if output_zip.exists():
        output_zip.unlink()

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
            f"Output: {output_zip}",
            "",
            "Excluded directories:",
            *[f"- {d}" for d in sorted(EXCLUDE_DIRS)],
            "",
            "Excluded extensions:",
            *[f"- {e}" for e in sorted(EXCLUDE_EXTENSIONS)],
            "",
        ]
    )
    info_path.write_text(info_text, encoding="utf-8")

    manifest_lines = [
        "Project_For_ChatGPT manifest",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"File count: {len(files) + 1}",
        "",
        INFO_NAME,
    ]

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(info_path, INFO_NAME)
        for file_path in sorted(files):
            arcname = file_path.relative_to(root).as_posix()
            zf.write(file_path, arcname)
            manifest_lines.append(arcname)
        zf.writestr(MANIFEST_NAME, "\n".join([*manifest_lines, ""]))

    manifest_path.write_text("\n".join([*manifest_lines, ""]), encoding="utf-8")
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
    print(f"{OUTPUT_DIR}\\{OUTPUT_NAME}")
    print("==========================================")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
