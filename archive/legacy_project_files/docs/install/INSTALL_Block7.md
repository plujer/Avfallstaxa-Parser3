# Install Block7 Semantic Parser

Packa upp ZIP-filen i projektets rot.

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Testa:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Commit:

```bat
git add .
git commit -m "Parser3 Block7 Semantic Parser"
git push
```
