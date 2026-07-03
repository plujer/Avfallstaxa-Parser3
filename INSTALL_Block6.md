# Install Block6 Golden Master Builder

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

Testa golden master builder:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --build-golden
```

Git:

```bat
git add .
git commit -m "Parser3 Block6 Golden Master Builder"
git push
```
