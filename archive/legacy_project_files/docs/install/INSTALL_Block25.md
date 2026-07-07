# Install Block25 Specific Match Fix

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug --trace
python -m pytest
build_report.bat
```

Commit:

```bat
git add .
git commit -m "Parser3 Block25 Specific Match Fix"
git push
```
