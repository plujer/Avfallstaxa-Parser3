# Install Block20 §6.1.2 Classifier + Aliases

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
git commit -m "Parser3 Block20 612 Classifier and Aliases"
git push
```
