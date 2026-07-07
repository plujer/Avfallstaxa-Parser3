
## Block48 – Project Cleanup and Legacy Archive Tool

- Added safe archive tool for legacy master files and historical install/changelog documents.
- Active v1.0 master sources remain unchanged and immutable.


## Block45.1 – Test Automation Stabilization
- Fixed `build_excel_report.bat` so `check_latest_run_status.py` no longer writes to the same file as shell redirection.
- Kept `run_project.bat` as the single normal verification command and ensured it prints the expected reportzip instruction.
- Restored semantic tax family bonus in `SemanticCandidateRanker`.
- Updated pipeline order test to reflect the new rule that pytest runs at the end of the full pipeline.
- Added `create_project_package.bat` for compact project ZIP creation when ChatGPT needs the current project.

# BLOCK_HISTORY

## Block45 – Developer Experience Test Automation

Fokus: Säker körning och tydlig teststatus.

- Tester körs automatiskt i `run_project.bat`.
- Commit skyddas av senaste pytest-status.
- Saknade rapportsteg från Block44 återställs.

## Block47 – Word Excel Mapping Engine

Fokus: Spårbar mappning från Word/parser till Taxepunkter.

- Varje Word/parser-taxa får ett stabilt internt `WordTaxID`.
- Mappning görs mot `Taxepunkter` via exakt radnyckel eller paragraf + taxepunkt.
- `MISSING` betyder att Word-raden saknar motsvarande Taxepunkter-rad.
- `REVIEW` betyder granskningsläge, inte automatiskt fel.
- Dubblettanvändning av samma EDP-taxa är tillåten så länge ingen annan konflikt finns.
- Projektpaket skapas automatiskt i `project_packages/` och skrivs över vid varje körning.
