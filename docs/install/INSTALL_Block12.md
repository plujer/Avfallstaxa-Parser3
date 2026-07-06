# Install Block12 Tax Classifier Precision

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Kör om rapporterna:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx"
```

Commit:

```bat
git add .
git commit -m "Parser3 Block12 Tax Classifier Precision"
git push
```
