# Block51 – Persistent Tax Identity Engine

## Syfte

Inför ett permanent internt ID för varje Word-taxepunkt. ID:t är baserat på taxepunktens innehåll och ska vara stabilt även om taxepunkten flyttas till en annan paragraf.

## Installera

Packa upp ZIP-filen i projektets rotmapp och skriv över befintliga filer när Windows frågar.

## Kör

```bat
run_project.bat
```

Skicka sedan tillbaka endast senaste ZIP-filen från:

```text
rapportzip\ExcelBuilder_Run_*.zip
```

## Nya rapporter

```text
output\excel\persistent_tax_identity_report.txt
output\excel\persistent_tax_identity.csv
output\excel\persistent_tax_identity_console.txt
```

## Commit

Kör inte `git_commit_block.bat` förrän ChatGPT har granskat rapportzipen och uttryckligen skriver att du ska köra commit-scriptet.
