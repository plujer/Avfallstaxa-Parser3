# Install Block21 Missing Row Diagnostics

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug
python -m pytest
build_report.bat
```

Commit:

```bat
git add .
git commit -m "Parser3 Block21 Missing Row Diagnostics"
git push
```
