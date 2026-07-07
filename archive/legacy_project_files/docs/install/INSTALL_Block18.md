# Install Block18 Acceptance Debug

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance-debug
python -m pytest
build_report.bat
```

Commit:

```bat
git add .
git commit -m "Parser3 Block18 Acceptance Debug"
git push
```
