# Install Block9 Hotfix

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
.venv\Scripts\activate
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Commit:

```bat
git add .
git commit -m "Fix context engine circular import"
git push
```
