# Excel Builder Block 22 – Knowledge Index

Detta block bygger ett mellanlager mellan Tax Knowledge och matchningsmotorn.

## Varför

I stället för att jämföra varje Word-taxa mot varje standardtaxa ska systemet först gruppera taxor efter strukturerad kunskap:

- kategori
- avfallstyp
- enhetstyp
- faktorhint
- behållarvolym

## Nya rapporter

```text
output/excel/knowledge_index_report.txt
output/excel/knowledge_index.csv
```

## Viktigt

Knowledge Index ändrar inte `Taxa_från_edp`.

Det är en förberedelse för en mer träffsäker regelmotor.

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
