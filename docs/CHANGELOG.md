
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

## Block47 – Word Excel Mapping Engine
- Added deterministic Word → Excel mapping engine with stable `WordTaxID` values.
- Added mapping reports: `word_excel_mapping_report.txt` and `word_excel_mapping.csv`.
- Documented that repeated use of the same EDP tax code by multiple Word rows is allowed and not an automatic error.
- Updated project package tool to write to `project_packages/Project_For_ChatGPT.zip` and overwrite the previous package.
- Added automatic project package creation at the end of the normal `run_project.bat` pipeline.
- Fixed latest test status parsing so `latest_run_status.txt` uses the final pytest summary, not earlier small summaries.

## Block50 – Word Excel Mapping 2.0

- Lade till sectionsoberoende `StableTaxIdentity` för Word-taxor.
- Lade till `ContentFingerprint` i Word→Excel-mappningen.
- Uppdaterade rapport och CSV för spårbarhet vid flyttade Word-paragrafer.
