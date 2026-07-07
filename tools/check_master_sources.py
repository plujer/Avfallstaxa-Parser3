from __future__ import annotations

from pathlib import Path
from excel_builder.config import MasterSourcesReader


def main() -> None:
    sources = MasterSourcesReader().read()
    out_dir = Path("output/diagnostics")
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "master_sources_report.txt"

    lines = [
        "Master Sources Report",
        "",
        f"Version: {sources.master_version}",
        f"Immutable: {sources.immutable}",
        f"Word master: {sources.word_master}",
        f"Word master exists: {sources.word_master.exists()}",
        f"Excel master: {sources.excel_master}",
        f"Excel master exists: {sources.excel_master.exists()}",
        "",
        "Protected sheets:",
    ]
    for rule in sources.protected_sheets:
        lines.append(f"- {rule.sheet_name}: {rule.protected_columns} | {rule.rule}")
    lines.extend([
        "",
        "Policy:",
        "- Masterfiler får aldrig skrivas över.",
        "- Om redigering behövs ska ny versionsfil skapas.",
        "- Taxepunkter A:E och hela Taxa_från_edp är skyddade skrivområden.",
    ])
    text = "\n".join(lines) + "\n"
    report.write_text(text, encoding="utf-8")
    print(text)
    if not sources.word_master.exists() or not sources.excel_master.exists():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
