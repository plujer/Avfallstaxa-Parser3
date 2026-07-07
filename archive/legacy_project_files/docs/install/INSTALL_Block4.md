# Install Block4 Tax Extractor

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

Testa extraktion:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --extract
```

Git:

```bat
git add .
git commit -m "Parser3 Block4 Tax Extractor"
git push
```
