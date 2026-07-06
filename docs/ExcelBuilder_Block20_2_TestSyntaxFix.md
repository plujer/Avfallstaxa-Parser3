# Excel Builder Block 20.2 – Test Syntax Fix

Detta block rättar syntaxfelet i:

```text
tests/test_tax_knowledge_cli_workbook.py
```

## Problem

Testet innehöll nästlade citattecken i en Python-sträng.

## Lösning

Testet kontrollerar nu delar av kommandot separat:

```python
assert "--workbook" in text
assert "ArbetsExcel_byggd_fran_parser.xlsx" in text
```

## Ny säkerhetskontroll

Ny fil:

```text
tools/check_test_syntax.py
```

Den körs före pytest i rapportbygget och kontrollerar att alla testfiler kan parsas.

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
