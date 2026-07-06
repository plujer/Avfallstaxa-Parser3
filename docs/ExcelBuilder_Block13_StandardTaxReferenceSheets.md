# Excel Builder Block 13 – Standard Tax Reference Sheets

Detta block lägger till den nya standardtaxefilen från programutvecklaren.

## Ny standardfil

```text
data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx
```

## Krav

Standardtaxorna ska bifogas som referensflikar i:

- arbetsdokumentet,
- Sorsele-output,
- Malå-output,
- Norsjö-output,
- alla framtida Excel Builder-output.

## Viktigt

Standardtaxor är **global kunskap**.

De får användas som stöd för att föreslå saknade taxekoder, men de är inte samma sak som kommunens faktiska EDP-export.

Kommununika filer ska fortfarande hållas isolerade:

```text
Sorsele EDP → Sorsele Excel
Malå EDP    → Malå Excel
Norsjö EDP  → Norsjö Excel
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
