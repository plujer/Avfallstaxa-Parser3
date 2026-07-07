from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ARCHIVE_ROOT = Path("archive/legacy_project_files")

LEGACY_FILES = [
    Path("data/ArbetsExcel_Reference.xlsx"),
    Path("data/master_templates/ArbetsExcel_Reference_v0.9.4_draft.xlsx"),
    Path("data/master_templates/ArbetsExcel_Template_v0.1.0_draft.xlsx"),
    Path("data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx"),
    Path("create_project_package_fixed.bat"),
    Path("run_block34_verification.bat"),
]

LEGACY_DIR_CONTENTS = [
    Path("docs/changelogg"),
    Path("docs/install"),
    Path("parser3/docs/changelogg"),
    Path("parser3/docs/install"),
    Path("tools/docs/changelogg"),
    Path("tools/docs/install"),
]

PLACEHOLDER_TEXT = """# Arkiverad mapp\n\nInnehållet i denna mapp har flyttats till `archive/legacy_project_files/`.\n\nMappen ligger kvar för bakåtkompatibilitet och tester som kontrollerar att\nrelease-mapparna finns kvar.\n"""

ROOT_README = """# Archive\n\nDenna mapp innehåller äldre projektfiler som inte längre ska användas aktivt.\n\nRegler:\n- Arkiverade filer får inte användas som aktiv projektkälla.\n- Aktiva masterfiler läses via `config/master_sources.json`.\n- `data/master_templates/ArbetsExcel_Template_v1.0.xlsx` och\n  `data/word_templates/Taxestruktur_Master_v1.0.docx` är aktiva masterfiler.\n"""


@dataclass(frozen=True)
class MoveResult:
    source: str
    destination: str
    status: str


def _unique_destination(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}__archive_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def archive_file(root: Path, rel_path: Path, results: list[MoveResult]) -> None:
    source = root / rel_path
    if not source.exists():
        results.append(MoveResult(str(rel_path), "", "missing"))
        return
    if not source.is_file():
        results.append(MoveResult(str(rel_path), "", "not_file"))
        return

    destination = root / ARCHIVE_ROOT / rel_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination = _unique_destination(destination)
    shutil.move(str(source), str(destination))
    results.append(MoveResult(str(rel_path), str(destination.relative_to(root)), "moved"))


def archive_directory_contents(root: Path, rel_dir: Path, results: list[MoveResult]) -> None:
    source_dir = root / rel_dir
    if not source_dir.exists():
        results.append(MoveResult(str(rel_dir), "", "missing"))
        return
    if not source_dir.is_dir():
        results.append(MoveResult(str(rel_dir), "", "not_dir"))
        return

    files = [p for p in source_dir.rglob("*") if p.is_file()]
    for source in files:
        # Do not move the placeholder if the tool is run again.
        if source.name == "README.md" and source.read_text(encoding="utf-8", errors="ignore").startswith("# Arkiverad mapp"):
            continue
        rel_file = source.relative_to(root)
        destination = root / ARCHIVE_ROOT / rel_file
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination = _unique_destination(destination)
        shutil.move(str(source), str(destination))
        results.append(MoveResult(str(rel_file), str(destination.relative_to(root)), "moved"))

    # Remove empty child directories but keep the root directory.
    for child in sorted(source_dir.rglob("*"), reverse=True):
        if child.is_dir():
            try:
                child.rmdir()
            except OSError:
                pass

    (source_dir / "README.md").write_text(PLACEHOLDER_TEXT, encoding="utf-8")


def write_manifest(root: Path, results: list[MoveResult]) -> Path:
    archive_root = root / ARCHIVE_ROOT
    archive_root.mkdir(parents=True, exist_ok=True)
    (root / "archive").mkdir(parents=True, exist_ok=True)
    (root / "archive" / "README.md").write_text(ROOT_README, encoding="utf-8")

    manifest = archive_root / "MANIFEST.md"
    lines = [
        "# Legacy project archive manifest",
        "",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Status | Source | Destination |",
        "|---|---|---|",
    ]
    for item in results:
        lines.append(f"| {item.status} | `{item.source}` | `{item.destination}` |")
    lines.append("")
    manifest.write_text("\n".join(lines), encoding="utf-8")
    return manifest


def archive_legacy_project_files(root: Path) -> list[MoveResult]:
    results: list[MoveResult] = []
    for rel_file in LEGACY_FILES:
        archive_file(root, rel_file, results)
    for rel_dir in LEGACY_DIR_CONTENTS:
        archive_directory_contents(root, rel_dir, results)
    write_manifest(root, results)
    return results


def main() -> int:
    root = Path.cwd().resolve()
    print("==========================================")
    print("Excel Builder - Archive Legacy Project Files")
    print("==========================================")
    print(f"Project root: {root}")
    print()

    results = archive_legacy_project_files(root)
    moved = sum(1 for r in results if r.status == "moved")
    missing = sum(1 for r in results if r.status == "missing")
    print(f"Moved: {moved}")
    print(f"Missing/skipped: {missing}")
    print(f"Manifest: {ARCHIVE_ROOT / 'MANIFEST.md'}")
    print()
    print("Kör sedan run_project.bat och skicka senaste rapportzip.")
    print("==========================================")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
