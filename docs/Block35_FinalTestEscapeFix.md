# Block 35 – Final Test Escape Fix

Detta block rättar det sista pytest-felet inför v1.0.0.

## Problem

Testet använde:

```python
"output\acceptance"
```

vilket Python tolkade som en sträng med escape-tecken (`\a` = bell).

## Lösning

Testet använder nu raw strings:

```python
r"output\acceptance"
r"output\word"
```

## Ingen parserlogik ändras

Detta block ändrar endast testfilen:

```text
tests/test_final_cleanup_before_release.py
```

## Kör

```bat
python -m pytest
build_report.bat
```
