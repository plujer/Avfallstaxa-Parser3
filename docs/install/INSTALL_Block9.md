# Install Block9 Context Engine

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

Testa kontext:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
```

Testa semantik:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Commit:

```bat
git add .
git commit -m "Parser3 Block9 Context Engine"
git push
```
