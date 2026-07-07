# Block49 – Pipeline Controller v1.0

## Syfte

Block49 inför en samlad pipeline-status så att `run_project.bat`, `git_commit_block.bat` och rapporteringen inte längre kan ge motstridiga resultat.

## Ändrade filer

```text
build_excel_report.bat
run_project.bat
git_commit_block.bat
tools/pipeline_status.py
tools/check_pipeline_commit_ready.py
tests/test_pipeline_status_controller.py
```

## Installation

Kopiera filerna till projektets rotmapp och skriv över befintliga filer.

## Körning

Kör endast:

```bat
run_project.bat
```

Skicka tillbaka:

```text
rapportzip\senaste ExcelBuilder_Run_*.zip
```

## Commitregel

Kör **inte** `git_commit_block.bat` förrän ChatGPT uttryckligen skriver att blocket är godkänt.

När blocket är godkänt kör du:

```bat
git_commit_block.bat
```

## Testat här

```text
353 passed, 3 warnings
```

## Git-kommandon

Efter godkänd körning och efter att ChatGPT säger till:

```bat
git_commit_block.bat
```

Kör inte `git_release_block.bat` ännu.
