# Excel Builder Block 20.1 – Knowledge Workbook Writer Fix

Detta block rättar importfelet från Block 20.

## Problem

`excel_builder/knowledge/__init__.py` importerade:

```text
knowledge_workbook_writer.py
```

men filen saknades.

## Lösning

Ny fil:

```text
excel_builder/knowledge/knowledge_workbook_writer.py
```

Den skapar fliken:

```text
Tax_Knowledge
```

i genererade arbetsböcker.

## Viktigt

Denna flik skrivs endast i genererade kopior/outputfiler.

Master-/templatearbetsboken ändras inte automatiskt.

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
