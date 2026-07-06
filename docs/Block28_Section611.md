# Block 28 – §6.1.1 Acceptance

Detta block lägger in radnivåfacit för §6.1.1 och åtgärdar den saknade split-raden.

## Facit §6.1.1

1. Verksamheter
2. Övriga abonnemangstyper
3. Vågkort
4. Borttappat vågkort
5. Ej redovisad ankomst till ÅVC (för företagare och privatpersoner som lämnar verksamhetsavfall utan att anmäla sin ankomst)
6. Ej redovisad eller fel redovisad fraktion av avfall

## Fix

Raden för “Ej redovisad ankomst till ÅVC …” ligger delad över två Word-stycken.
`Section611Extractor` kombinerar de två styckena och exporterar den som en taxarad.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug --trace
python -m pytest
build_report.bat
```

ZIP skapas fortfarande automatiskt i `output`.
