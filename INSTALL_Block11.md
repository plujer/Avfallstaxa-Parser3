# Install Block11 Diff Engine

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Kör förklaringsrapport:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain
```

Kör diff mot Excel:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx"
```

Commit:

```bat
git add .
git commit -m "Parser3 Block11 Diff Engine"
git push
```
