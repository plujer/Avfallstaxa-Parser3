# Install Block15 Build System

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör sedan:

```bat
build_report.bat
```

Det skapar en ZIP i output-mappen.

Om du vill köra manuellt:

```bat
python -m pytest -v --tb=short > output\pytest_report.txt 2>&1
```

Commit:

```bat
git add .
git commit -m "Parser3 Block15 Build System"
git push
```
