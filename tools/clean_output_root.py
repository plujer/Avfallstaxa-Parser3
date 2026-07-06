"""Remove stale report files from output root before a run.

Older build scripts wrote reports directly into output/. Newer scripts write to
subfolders. This cleanup prevents old root files from confusing the run ZIP.
"""

from __future__ import annotations

from pathlib import Path


ROOT_FILES = [
    "environment_report.txt",
    "master_console.txt",
    "master_profile_report.txt",
    "parser3_architecture_report.txt",
    "parser3_explain_report.txt",
    "parser3_precision_report.txt",
    "parser3_report.txt",
    "parser3_result.json",
    "parser3_trace_report.txt",
    "parser_console.txt",
    "pytest_report.txt",
    "parser_facit_generated.yaml",
]


def main() -> None:
    output = Path("output")
    output.mkdir(exist_ok=True)

    removed = 0
    for filename in ROOT_FILES:
        path = output / filename
        if path.exists() and path.is_file():
            path.unlink()
            removed += 1

    print(f"Stale root output files removed: {removed}")


if __name__ == "__main__":
    main()
