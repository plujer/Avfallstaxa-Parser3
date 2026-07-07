# Block45.2 – Commit guard PermissionError fix

## Syfte

Rättar felet där `git_commit_block.bat` låste `output\diagnostics\latest_run_status.txt` genom att både omdirigera Python-output till filen och låta Python-scriptet skriva till samma fil.

## Ändrade filer

- `tools/check_latest_run_status.py`
- `git_commit_block.bat`

## Installera

Kopiera filerna till projektets rot och skriv över befintliga filer.

## Kör

1. Kör inte om hela projektet om senaste `run_project.bat` redan visar `Tests: OK`, `Passed: 344`, `Failed: 0`.
2. Kör:

```bat
git_commit_block.bat
```

## Om felet ändå kvarstår

Stäng program som kan ha öppnat `output\diagnostics\latest_run_status.txt`, exempelvis Notepad, Excel eller VS Code, och kör igen.
