# Install Excel Builder Block 20.3 – Knowledge Token and Project Scope Fix

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

## Kontrollera testsyntax

```bat
python tools\check_test_syntax.py
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

Skicka senaste ZIP-filen från:

```text
rapportzip/
```

## Git add

```bat
git add .
```

## Git commit

```bat
git commit -m "Excel Builder Block20.3 Knowledge Token and Project Scope Fix"
```

## Git push

```bat
git push
```
