# Install Block8 Section Engine Rewrite

Packa upp ZIP-filen i projektets rot:

```text
C:\PyProjects\Taxa 3.0
```

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Testa mot dokument:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Commit:

```bat
git add .
git commit -m "Parser3 Block8 Section Engine Rewrite"
git push
```
