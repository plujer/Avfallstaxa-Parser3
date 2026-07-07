# Excel Builder Block 29 – Semantic Decision Integration

Detta block kopplar ihop Semantic Candidate Ranking med Decision Engine.

## Ny beslutslogik

Besluten använder nu topprankade semantiska kandidater.

Källprioritet:

```text
1. Kommunens EDP
2. Taxepunkter med taxekod
3. Standardtaxor
4. Taxepunkter utan taxekod / övrigt beslutsstöd
```

## Nya principer

- Kandidater utan taxekod blir aldrig automatiska taxekodsbeslut.
- Om toppkandidater ligger för nära varandra blir beslutet `REVIEW_REQUIRED`.
- Standardtaxor är fortfarande bara förslag.
- `Taxa_från_edp` ändras inte.

## Nya rapporter

```text
output/excel/tax_decision_semantic_report.txt
output/excel/tax_decision_semantic_results.csv
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
