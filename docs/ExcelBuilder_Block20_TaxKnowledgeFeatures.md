# Excel Builder Block 20 – Tax Knowledge Features

Detta block startar Tax Knowledge Engine.

## Syfte

I stället för att bara jämföra textnamn ska systemet först strukturera varje Word/parser-taxa.

Exempel på extraherad kunskap:

- kapitel/paragrafgrupp
- kategori
- avfallstyp
- enhetstyp
- behållarvolym
- faktorhint
- nyckelord
- confidence

## Nya rapporter

```text
output/excel/tax_knowledge_report.txt
output/excel/tax_knowledge_features.csv
```

## Viktigt

Detta block ändrar inte EDP och skriver inte taxekoder.

Det skapar bara strukturerad kunskap som nästa matchningsmotor kan använda.

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
