# Excel Builder Block 01 – Bootstrap

Detta startar nästa fas efter Parser3 v1.0.0.

## Syfte

Excel Builder läser parserns verifierade output:

```text
output/reports/parser3_result.json
```

och skapar en ny arbets-Excel:

```text
output/excel/ArbetsExcel_byggd_fran_parser.xlsx
```

## Viktigt

Den skapade Excel-filen är **arbets-Excel**.

Den är inte master förrän användaren uttryckligen godkänner den.

## Kör

Först parserrapport:

```bat
build_report.bat
```

Sedan Excel Builder:

```bat
build_excel.bat
```

eller direkt:

```bat
python excel_builder_cli.py
```
