# ExcelBuilder Block51 – Persistent Tax Identity Engine

## Syfte

Block51 inför ett permanent internt ID för varje taxepunkt från Word-mastern.

ID:t ska vara stabilt när en taxepunkt flyttas mellan paragrafer men fortfarande har samma verksamhetsmässiga innebörd.

## Regler

- `PersistentTaxID` är inte en EDP-taxekod.
- `Taxa_från_edp` är fortsatt facit och får aldrig ändras.
- Word-master och Excel-master är immutable.
- Dubbletter av samma innehåll är granskningsinformation, inte automatiskt fel.

## Output

```text
output/excel/persistent_tax_identity_report.txt
output/excel/persistent_tax_identity.csv
output/excel/persistent_tax_identity_console.txt
```

## Pipeline

Steget körs efter Word → Excel Mapping och innan isolerad kommunprojektkörning.
