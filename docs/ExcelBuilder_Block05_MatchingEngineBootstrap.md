# Excel Builder Block 05 – Matching Engine Bootstrap

Detta block startar Matching Engine.

## Syfte

Läsa:

```text
output/reports/parser3_result.json
data/ArbetsExcel_Reference.xlsx
```

och skapa en matchningsrapport:

```text
output/excel/excel_matching_report.txt
output/excel/excel_matching_results.csv
```

## Statusar

- `EXACT` – säker träff på paragraf + taxapunkt + variant + enhet
- `PROBABLE` – träff på paragraf + taxapunkt men variant/enhet skiljer
- `REVIEW` – fuzzy eller dubblett, kräver manuell kontroll
- `NEW` – saknas i arbets-Excel och behöver skapas

## Viktigt

Detta block är läsande. Det skriver inte till referensarbetsboken.

## Rapport efter varje block

Kör:

```bat
build_excel_report.bat
```

Skicka senaste ZIP-filen från:

```text
rapportzip/
```
