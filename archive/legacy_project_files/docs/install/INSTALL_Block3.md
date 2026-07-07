# Install Block3 Table Engine

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

Testa tabellmotor:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --tables
```

Git:

```bat
git add .
git commit -m "Parser3 Block3 Table Engine"
git push
```
