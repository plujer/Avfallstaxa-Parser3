# Excel Builder Block 14 – Proposal and Trace Sheets

Detta block lägger till två standardflikar i alla genererade arbetsböcker.

## Nya flikar

```text
Taxa_Förslag
Regelspårning
```

## Taxa_Förslag

Här ska systemet senare samla förslag på taxekoder som saknas i kommunens `Taxa_från_edp`.

Exempel på källa:

- EDP standardtaxor
- generella regelverk
- manuell granskning

Förslag är inte samma sak som bekräftad EDP-kod.

## Regelspårning

Här ska systemet senare dokumentera hur varje rad och fält byggdes.

Exempel:

- Word/parser
- EDP-exakt match
- standardtaxeförslag
- manuell granskning

## Viktigt

Dessa flikar ska finnas i:

- `ArbetsExcel_byggd_fran_parser.xlsx`
- Sorsele-output
- Malå-output
- Norsjö-output
- alla framtida Excel Builder-output

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
