# Excel Builder Block 05.1 – Test Syntax Fix

Detta block rättar endast syntaxfelet i:

```text
tests/test_excel_report_zip_scripts.py
```

## Problem

Testet innehöll ogiltig Python-syntax:

```python
assert "$zipDir = "rapportzip"" in text
```

## Lösning

Testet kontrollerar nu `rapportzip` utan nästlade citattecken.

## Kör

```bat
python -m pytest
build_excel_report.bat
```

Skicka sedan senaste ZIP-filen från:

```text
rapportzip/
```
