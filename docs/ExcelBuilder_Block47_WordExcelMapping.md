# Block47 – Word Excel Mapping Engine

## Syfte

Block47 inför ett deterministiskt spårbarhetslager mellan Word/parser-taxor och rader i `Taxepunkter`.

Varje Word/parser-rad får ett stabilt internt ID, `WordTaxID`, och kopplas till motsvarande Excel-rad där det är möjligt.

## Viktiga regler

- Word-master är read-only och ändras aldrig.
- Excel-master är read-only och ändras aldrig.
- `Taxepunkter` A:E ändras aldrig automatiskt.
- `Taxa_från_edp` ändras aldrig.
- Samma EDP-taxa kan förekomma på flera Word-rader utan att det automatiskt är fel.

## Nya rapporter

```text
output/excel/word_excel_mapping_report.txt
output/excel/word_excel_mapping.csv
output/excel/word_excel_mapping_console.txt
```

## Statusvärden

- `MAPPED` – Word-raden har en matchande rad i `Taxepunkter`.
- `REVIEW` – flera möjliga rader finns och bör granskas.
- `MISSING` – Word-raden saknar motsvarande rad i `Taxepunkter`.

## Projektpaket

`tools/create_project_package.py` skapar nu:

```text
project_packages/Project_For_ChatGPT.zip
```

Filen skrivs över vid varje körning så att mappen inte växer okontrollerat.
