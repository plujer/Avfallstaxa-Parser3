
## Block45.1 – Test Automation Stabilization
- Fixed `build_excel_report.bat` so `check_latest_run_status.py` no longer writes to the same file as shell redirection.
- Kept `run_project.bat` as the single normal verification command and ensured it prints the expected reportzip instruction.
- Restored semantic tax family bonus in `SemanticCandidateRanker`.
- Updated pipeline order test to reflect the new rule that pytest runs at the end of the full pipeline.
- Added `create_project_package.bat` for compact project ZIP creation when ChatGPT needs the current project.

# CHANGELOG

## Block45 – Developer Experience Test Automation

- `run_project.bat` kör nu hela pipeline och därefter hela pytest-sviten automatiskt.
- `build_excel_report.bat` återställer saknade rapportsteg från Block36–Block40.
- `git_commit_block.bat` stoppar commit om senaste testresultat inte är godkänt.
- Rapportzip inkluderar `latest_run_status.txt`.
- Dokumenterat att legitim dubblettkoppling Word-rad → samma EDP-taxa inte är fel i sig.
