# Install Excel Builder Block 23 – Master Rule Repository

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
git commit -m "Excel Builder Block23 Master Rule Repository"
```

## Git push

```bat
git push
```
