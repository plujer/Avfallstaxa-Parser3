"""Organize output files into stable report folders."""

from __future__ import annotations

from pathlib import Path
import shutil


OUTPUT = Path("output")

FOLDERS = {
    "acceptance": [
        "parser3_acceptance_report.txt",
        "parser3_acceptance_debug_report.txt",
        "parser3_missing_diagnostics.txt",
    ],
    "diagnostics": [
        "parser_console.txt",
        "environment_report.txt",
        "master_console.txt",
        "pytest_report.txt",
    ],
    "trace": [
        "parser3_trace_report.txt",
    ],
    "reports": [
        "parser3_report.txt",
        "parser3_result.json",
        "parser3_architecture_report.txt",
        "parser3_explain_report.txt",
        "parser3_precision_report.txt",
        "master_profile_report.txt",
    ],
    "excel": [],
    "word": [],
    "archive": [],
}


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)

    for folder in FOLDERS:
        (OUTPUT / folder).mkdir(parents=True, exist_ok=True)

    for folder, filenames in FOLDERS.items():
        for filename in filenames:
            src = OUTPUT / filename
            dst = OUTPUT / folder / filename
            if src.exists():
                if dst.exists():
                    dst.unlink()
                shutil.move(str(src), str(dst))

    print("Output organized.")


if __name__ == "__main__":
    main()
