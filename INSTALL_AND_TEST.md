# Block46 – Project Package Output Integration

## Syfte

- Flyttar `Project_For_ChatGPT.zip` från projektroten till `project_packages/Project_For_ChatGPT.zip`.
- `project_packages` exkluderas från paketet så gamla projektpaket inte packas in igen.
- Paketet skrivs över vid varje körning, så det inte byggs upp flera stora ZIP-filer.
- `build_excel_report.bat` / `run_project.bat` skapar automatiskt aktuellt projektpaket i slutet av körningen.

## Ändrade filer

- `tools/create_project_package.py`
- `create_project_package.bat`
- `build_excel_report.bat`
- `tests/test_project_package_tool.py`
- `tests/test_project_metadata.py`
- `version.json`
- `docs/PROJECT_STATUS.md`
- `docs/CHANGELOG.md`
- `docs/history/BLOCK_HISTORY.md`

## Installation

Kopiera innehållet i paketet till projektets rotmapp och ersätt befintliga filer.

## Test

Kör:

```bat
run_project.bat
```

Den ska nu både skapa rapportzip och uppdatera:

```text
project_packages\Project_For_ChatGPT.zip
```

## Skicka tillbaka

Skicka endast senaste:

```text
rapportzip\ExcelBuilder_Run_*.zip
```
