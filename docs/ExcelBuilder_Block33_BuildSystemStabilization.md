# Excel Builder Block 33 – Build System Stabilization

Detta block återställer den fullständiga rapportpipelinen efter Block 32.

## Problem

Block 32 ersatte av misstag den avancerade `build_excel_report.bat` med en minimal specifikationskörning.

Det gjorde att många rapportsteg saknades.

## Lösning

`build_excel_report.bat` är nu full pipeline igen och innehåller dessutom:

```text
python tools\check_v1_spec.py
```

som första steg.

## Viktigt

v1.0-specifikationen är nu ett tillägg, inte en ersättning.

## Körordning

```text
1. v1.0-specifikation
2. testsyntax
3. pytest
4. context resolver
5. schema scan
6. standard catalog scan
7. tax code intelligence
8. semantic pipeline
9. decisions
10. coverage
11. Sorsele project run
12. report zip
```
