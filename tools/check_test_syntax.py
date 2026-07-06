"""Check that all test files can be parsed by Python.

This catches pure syntax errors before pytest collection fails with less useful
side effects.
"""

from __future__ import annotations

from pathlib import Path
import ast
import sys


def main() -> int:
    errors: list[str] = []

    for path in sorted(Path("tests").rglob("test_*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}: line {exc.lineno}: {exc.msg}")

    if errors:
        print("Syntax errors in test files:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("All test files parsed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
