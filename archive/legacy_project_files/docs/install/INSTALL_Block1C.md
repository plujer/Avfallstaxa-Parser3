# Install Block1C Document Engine

Packa upp ZIP-filen i projektets rot:

```text
C:\PyProjects\Taxa 3.0
```

Aktivera miljön:

```bat
.venv\Scripts\activate
```

Installera beroenden:

```bat
python -m pip install -r requirements.txt
```

Verifiera:

```bat
python run.py
pytest
```

Testa med Word-fil:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx"
```

Git:

```bat
git add .
git commit -m "Parser3 Block1C Document Engine"
git push
```
