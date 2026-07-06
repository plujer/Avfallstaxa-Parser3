"""Clean duplicate nested test folders created by accidental ZIP extraction.

The canonical test folder is:
    tests/

The following nested folder is invalid and can cause pytest import mismatch:
    tests/tests/
"""

from __future__ import annotations

from pathlib import Path
import shutil


def main() -> None:
    nested = Path("tests") / "tests"

    if nested.exists() and nested.is_dir():
        shutil.rmtree(nested)
        print(f"Removed duplicate nested test folder: {nested}")
    else:
        print("No duplicate nested test folder found.")

    duplicates = find_duplicate_test_filenames(Path("tests"))
    if duplicates:
        print("Duplicate test filenames found:")
        for filename, paths in duplicates.items():
            print(f"- {filename}")
            for path in paths:
                print(f"  {path}")
    else:
        print("No duplicate test filenames found.")


def find_duplicate_test_filenames(root: Path) -> dict[str, list[Path]]:
    files: dict[str, list[Path]] = {}

    if not root.exists():
        return {}

    for path in root.rglob("test_*.py"):
        files.setdefault(path.name, []).append(path)

    return {name: paths for name, paths in files.items() if len(paths) > 1}


if __name__ == "__main__":
    main()
