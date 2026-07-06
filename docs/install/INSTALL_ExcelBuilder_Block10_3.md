# Install Excel Builder Block 10.3 – Repository Cleanup

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

## Rensa teststruktur

```bat
python tools\cleanup_duplicate_tests.py
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
git commit -m "Excel Builder Block10.3 Repository Cleanup"
```

## Git push

```bat
git push
```
