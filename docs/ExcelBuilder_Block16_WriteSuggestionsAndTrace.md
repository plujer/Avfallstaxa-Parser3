# Excel Builder Block 16 – Write Suggestions and Trace

Detta block börjar fylla de nya arbetsflikarna.

## Vad blocket gör

Standardtaxeförslag skrivs till:

```text
Taxa_Förslag
```

Beslutsunderlag skrivs till:

```text
Regelspårning
```

## Viktigt

Detta block ändrar inte `Taxa_från_edp`.

Standardtaxor får endast skrivas som förslag/spårning.

## Nytt kommando

```bat
python excel_builder_apply_suggestions.py --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx"
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
