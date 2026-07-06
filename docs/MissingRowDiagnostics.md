# Block 21 – Missing Row Diagnostics

Detta block skapar en ny rapport:

```text
output\parser3_missing_diagnostics.txt
```

Rapporten visar för varje saknad facitrad:

- exakt semantisk träff,
- fuzzy semantisk träff,
- närliggande rader med gemensamma ord,
- liknande exporterade rader.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug
python -m pytest
build_report.bat
```
