# Block 24 – Extractor Trace

Detta block instrumenterar `Section612Extractor`.

## Ny rapport

```text
output\parser3_trace_report.txt
```

Rapporten visar:

- input-text
- normaliserad text
- bästa facitmatchning
- score
- beslut: exported / not_exported
- orsak
- document order

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug --trace
python -m pytest
build_report.bat
```
