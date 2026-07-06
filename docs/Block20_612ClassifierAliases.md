# Block 20 – §6.1.2 Classifier + Acceptance Aliases

Detta block åtgärdar två saker:

1. Block A i §6.1.2 kan exporteras även när Word-raden saknar synlig prisindikator.
2. Acceptance-jämförelsen får normalisering/alias för små textskillnader.

## Viktigt

Detta gäller bara parserns verifiering mot facit. Arbets-Excel är fortfarande inte facit.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance-debug
python -m pytest
build_report.bat
```
