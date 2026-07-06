# Parser 3.1 – Architecture Cleanup

Detta block inför en enda officiell pipeline:

```text
DocumentReader
  -> ContextEngine
  -> SemanticParser
  -> Unified extractors
  -> Export
```

## Viktiga ändringar

- CLI använder nu `TaxPipeline`.
- `FlatTaxExtractor` hanterar visuella tabellrader som Word ger som stycken.
- Pris tas bort från `name`.
- Rader med flera priser blir flera taxerader.
- Uppenbara fortsättningsfragment filtreras bort.

## Kör

```bat
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx"
```
