# Excel Builder Block 13.1 – Project Test Cleanup

Detta block rättar testinsamlingen efter Block 13.

## Problem

`tests/test_project_scripts.py` innehöll Windows-sökvägar med enkla backslashar:

```python
"output\projects\Sorsele"
```

När de inte skrivs som raw strings kan Python tolka sekvenser som `\p` som ogiltiga escape-sekvenser.

## Lösning

Testet använder nu raw strings:

```python
r"output\projects\Sorsele"
```

## Ingen produktionslogik ändras

Detta block ändrar endast testfilen:

```text
tests/test_project_scripts.py
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
