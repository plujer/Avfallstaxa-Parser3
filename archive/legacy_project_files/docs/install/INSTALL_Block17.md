# Install Block17 Parser Acceptance

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance
python -m pytest
build_report.bat
```

Commit:

```bat
git add .
git commit -m "Parser3 Block17 Parser Acceptance"
git push
```
