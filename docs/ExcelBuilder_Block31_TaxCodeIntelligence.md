# Excel Builder Block 31 – Tax Code Intelligence

Detta block börjar tolka EDP-taxekoder som strukturerad kunskap.

## Exempel

```text
KÄ240RM26FV
```

tolkas som:

```text
prefix = KÄ
container_type = Kärl
volume = 240
waste_code = RM
interval = 26
variant = FV
family_key = KÄ240RM
```

## Nya rapporter

```text
output/excel/tax_code_intelligence_report.txt
output/excel/tax_code_intelligence.csv
```

## Viktigt

Taxekoderna ändras inte.

Detta är endast tolkning/kunskapsutvinning.

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
