# Install Block2 Heading Tree

Packa upp ZIP-filen i projektets rot:

```text
C:\PyProjects\Taxa 3.0
```

Aktivera miljön:

```bat
.venv\Scripts\activate
```

Verifiera:

```bat
python run.py
python -m pytest
```

Testa med Word-fil:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --headings
```

Git:

```bat
git add .
git commit -m "Parser3 Block2 Heading Tree Builder"
git push
```
