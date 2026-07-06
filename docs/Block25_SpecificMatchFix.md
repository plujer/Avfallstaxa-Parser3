# Block 25 – Specific Match Fix

Detta block åtgärdar den sista kända buggen i §6.1.2-matchningen.

## Problem

Kortare facitnamn kunde vinna över längre namn eftersom tidigare logik bröt på första delsträngsträff:

```text
Avfall till energiåtervinning
```

vann över:

```text
Skrymmande avfall till energiåtervinning större än 20×20×80
```

## Lösning

`Section612Extractor` matchar nu i ordningen:

1. exakt normaliserad matchning,
2. längsta delsträngsträff,
3. fuzzy fallback.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug --trace
python -m pytest
build_report.bat
```
