# Excel Builder Block 10 – Taxepunkter Row Builder

Detta block ändrar arkitekturen enligt grundkravet:

> Word/parsern avgör vilka taxor som ska finnas som rader i `Taxepunkter`.

EDP används senare för att komplettera raderna, men EDP avgör inte om raden ska finnas.

## Ny pipeline

```text
Parser rows
   ↓
Taxepunkter Row Builder
   ↓
REUSE befintlig rad
CREATE ny rad
REVIEW osäker dubblett
   ↓
EDP-komplettering senare
```

## Nya rapporter

```text
output/excel/taxepunkter_row_plan_report.txt
output/excel/taxepunkter_row_plan.csv
```

## Kör tester

```bat
python -m pytest
```

## Bygg rapportpaket

```bat
build_excel_report.bat
```

## Skicka tillbaka

```text
rapportzip/
```
