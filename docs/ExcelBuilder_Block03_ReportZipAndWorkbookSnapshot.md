# Excel Builder Block 03 – Report ZIP + Workbook Snapshot

Detta block gör två saker:

1. Skapar en tydlig rapport-ZIP automatiskt för det jag vill se efter varje Excel Builder-block.
2. Skapar en snapshot av viktiga blad i Arbets-Excel så vi kan bygga Matching Engine på verkliga rader.

## Nytt kommando för återrapportering

Efter varje Excel Builder-block ska du köra:

```bat
build_excel_report.bat
```

Den skapar en ZIP i:

```text
rapportzip/
```

Skicka den senaste ZIP-filen till ChatGPT.

## Ny snapshot

```text
output/excel/arbets_excel_snapshot.txt
```

Den innehåller radexempel från:

- Taxepunkter
- Taxa_från_edp
- Taxa_Saknas
- Kontrollrapport

## Varför

Nästa steg är Matching Engine. Då behöver jag se både strukturprofil och verkliga rader.
