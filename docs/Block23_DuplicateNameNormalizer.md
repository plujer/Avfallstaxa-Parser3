# Block 23 – Duplicate Name Normalizer

Detta block riktar in sig på den sista saknade raden i §6.1.2.

## Problem

Word kan läsa en tabellrad ungefär så här:

```text
Skrymmande avfall ... 20*20*80
Skrymmande avfall ... 20*20*80
200307 200307
kilogram kilogram
```

Det är samma taxapunkt dubblerad med metadata efteråt.

## Lösning

`NameNormalizer` tar nu bort metadata först och kollapsar därefter dubblerade namnsekvenser.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug
python -m pytest
build_report.bat
```
