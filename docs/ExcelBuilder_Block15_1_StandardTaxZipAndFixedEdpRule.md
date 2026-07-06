# Excel Builder Block 15.1 – Standard Tax ZIP + Fixed EDP Rule

Detta block rättar regressionen från Block 15 och lägger in en tydlig regel:

> Taxor som redan finns i `Taxa_från_edp` är fasta och ska inte ändras automatiskt.

## Fix 1 – rapport-ZIP

`tools/zip_excel_report.ps1` inkluderar återigen:

```text
data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx
```

## Fix 2 – ny avvikelseflik

Alla genererade arbetsböcker får nu även:

```text
EDP_Avviker_Standard
```

Den ska senare användas för att visa när en kommun-EDP avviker från standardtaxa.

## Viktigt

Standardtaxor får användas som:

- förslag,
- avvikelseanalys,
- stöd vid saknade taxor.

Standardtaxor får inte skriva över befintliga taxor i `Taxa_från_edp`.

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
