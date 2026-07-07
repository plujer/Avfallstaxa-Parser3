# Block36 – Tax Family Intelligence

## Syfte

Block36 inför ett beslutsstöd som grupperar taxekoder i familjer. Exempelvis ska `KÄ240RM26`, `KÄ240RM52`, `KÄ240RM104`, `KÄ240RMFV` och `KÄ240RMFRI` förstås som samma grundfamilj `KÄ240RM`, men med olika intervall eller varianter.

## Viktiga regler

- `Taxa_från_edp` är fortsatt facit och ändras aldrig automatiskt.
- Standardtaxor används endast som globalt beslutsstöd.
- Kommunprojekten Sorsele, Malå och Norsjö hålls separata.
- Tax Family Intelligence får endast förbättra förslag, matchning och rapportering.

## Tekniskt innehåll

Nya komponenter:

- `excel_builder/tax_family/tax_family_parser.py`
- `excel_builder/tax_family/tax_family_repository.py`
- `excel_builder/tax_family/tax_family_matcher.py`
- `excel_builder_tax_family.py`
- `excel_builder/reports/tax_family_reporter.py`

Rapporter:

- `output/excel/tax_family_report.txt`
- `output/excel/tax_families.csv`
- `output/excel/tax_family_console.txt`

## Verifiering

Blocket verifieras genom:

```bat
run_project.bat
```

Om projektkörningen själv anger att tester behöver köras separat:

```bat
run_tests.bat
```
