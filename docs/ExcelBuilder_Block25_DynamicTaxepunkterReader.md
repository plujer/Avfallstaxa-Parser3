# Excel Builder Block 25 – Dynamic Taxepunkter Reader

Detta block rättar huvudfelet från Block 24.

## Problem

Workbook Schema Scanner visade att `Taxepunkter` har rubrikrad på rad 5.

Tidigare läste Rule Repository rubriker från rad 1. Därför blev:

```text
Taxepunkt rules: 0
```

## Lösning

Ny läsare:

```text
DynamicTaxepunkterReader
```

Den använder:

```text
WorkbookSchemaScanner
```

för att hitta korrekt rubrikrad och läsa `Taxepunkter` dynamiskt.

## Förväntad effekt

`Taxepunkt rules` bör inte längre vara 0.

## Viktigt

Masterarbetsboken ändras inte.

Den läses endast.

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
