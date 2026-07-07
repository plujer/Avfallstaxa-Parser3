- Block46: Project package output now goes to `project_packages/Project_For_ChatGPT.zip`; `run_project.bat` refreshes it at the end of every successful pipeline run.

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
