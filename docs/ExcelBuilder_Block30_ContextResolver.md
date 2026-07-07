# Excel Builder Block 30 – Context Resolver

Detta block börjar förbättra Word-förståelsen.

## Problem

Många parserrader är korta eller rubriklika, exempelvis:

```text
En- och tvåbostadshus
Kärl 240 l
```

De behöver kontext från omgivande rader och sektioner.

## Lösning

Ny komponent:

```text
ParserContextResolver
```

Den berikar parserrader med:

- sektion/kategori,
- fastighetstyp,
- avfallstyp,
- tjänstetyp,
- behållartyp.

## Nya rapporter

```text
output/excel/context_resolution_report.txt
output/excel/context_resolved_rows.csv
```

## Viktigt

Originalparsern ändras inte.

`Taxa_från_edp` ändras inte.

Kontext används som förbättrat beslutsunderlag.

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
