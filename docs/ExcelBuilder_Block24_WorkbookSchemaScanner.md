# Excel Builder Block 24 – Workbook Schema Scanner

Detta block gör en djupare inventering av masterarbetsboken.

## Syfte

Innan vi bygger en dynamisk Taxepunkter-läsare behöver vi veta hur arbetsboken faktiskt ser ut.

Scannern läser:
- alla blad
- synlighet
- rader/kolumner
- möjliga rubrikrader
- Excel-tabeller
- formler
- datavalideringar
- dolda kolumner/rader
- merged cells
- freeze panes
- autofilter
- namngivna områden

## Viktigt

Scannern ändrar inte masterarbetsboken.

## Nya rapporter

```text
output/excel/workbook_schema_report.txt
output/excel/workbook_schema_sheets.csv
output/excel/workbook_schema_header_candidates.csv
```

## Nästa steg

När rapporten visar rätt rubrikrad för `Taxepunkter` går vi vidare till:

```text
Block 25 – Dynamic Taxepunkter Reader
```
