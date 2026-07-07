"""Validate that v1.0 specification files exist and contain key invariants."""

from __future__ import annotations

from pathlib import Path


REQUIRED_FILES = [
    Path("docs/spec/ExcelBuilder_v1_0_Specification.md"),
    Path("docs/spec/ExcelBuilder_v1_0_Roadmap.md"),
    Path("docs/spec/ExcelBuilder_v1_0_Invariants.md"),
]

REQUIRED_TERMS = [
    "Taxa_från_edp får inte ändras automatiskt",
    "Kommunens EDP är facit",
    "Kunskap delas",
    "data delas inte",
    "NOT_A_TAXA",
    "Document Structure Engine",
    "Tax Family Intelligence",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Missing specification files:")
        for path in missing:
            print(f"- {path}")
        return 1

    combined = "\n".join(path.read_text(encoding="utf-8") for path in REQUIRED_FILES)
    missing_terms = [term for term in REQUIRED_TERMS if term not in combined]
    if missing_terms:
        print("Missing required terms:")
        for term in missing_terms:
            print(f"- {term}")
        return 1

    print("v1.0 specification validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
