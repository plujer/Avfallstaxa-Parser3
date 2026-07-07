# Install Block10 Heading Numbering

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Testa mot dokumentet:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Commit:

```bat
git add .
git commit -m "Parser3 Block10 Heading Numbering"
git push
```
