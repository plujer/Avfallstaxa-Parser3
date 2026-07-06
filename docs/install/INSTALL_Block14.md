# Install Block14 Parser 3.1 Architecture Cleanup

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
.venv\Scripts\activate
python run.py
python -m pytest
```

Kör pipeline-rapport:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture
```

Kör diff:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx"
```

Commit:

```bat
git add .
git commit -m "Parser3 Block14 Architecture Cleanup"
git push
```
