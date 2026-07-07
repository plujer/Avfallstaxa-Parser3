# Excel Builder Block 26 – Standard Tax Catalog Reverse Engineering

Detta block analyserar standardtaxefilen på samma sätt som vi analyserade masterarbetsboken.

## Syfte

Standardtaxefilen innehåller sannolikt fler logiska sektioner än den gamla läsaren hittade.

Därför gör vi nu:

- schemaanalys av standardtaxefilen,
- identifiering av flera sektioner per flik,
- förbättrad `StandardTaxReader`,
- genererad normaliserad standardtaxefil.

## Ny normaliserad fil

```text
output/excel/EDP_Standardtaxor_normalized.xlsx
```

Originalfilen ändras inte.

## Viktigt

Standardtaxor är fortfarande referens/förslag.

De får aldrig skriva över `Taxa_från_edp`.

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
