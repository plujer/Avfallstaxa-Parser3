# Block43 – Master Source Integration & Immutable Template Guard

## Syfte

Block43 gör de nya masterfilerna till projektets officiella källor och inför tekniska spärrar så att de aldrig skrivs över.

## Nya masterkällor

- `data/word_templates/Taxestruktur_Master_v1.0.docx`
- `data/master_templates/ArbetsExcel_Template_v1.0.xlsx`

## Viktiga regler

- Masterfilerna är immutable.
- Om en ändring behövs ska en ny versionsfil skapas.
- `Taxepunkter!A:E` får inte skrivas automatiskt.
- `Taxa_från_edp` får inte skrivas automatiskt alls.
- Projektet ska alltid arbeta på kopior av vald Excel-master.

## Installera

Packa upp ZIP-filen i projektets rotkatalog och låt filer skrivas över där det efterfrågas.

## Kör

Kör alltid först:

```bat
run_project.bat
```

Endast om `run_project.bat` själv säger att tester behövs:

```bat
run_tests.bat
```

## Skicka tillbaka

Skicka endast senaste ZIP-filen från:

```text
rapportzip\ExcelBuilder_Run_*.zip
```

## Git efter godkännande

Efter att blocket är godkänt:

```bat
git_commit_block.bat
```

Kör inte release förrän du får klartecken:

```bat
git_release_block.bat
```

## Lokal verifiering i detta paket

Följande kördes lokalt:

```text
python -m pytest -q
292 passed
```
