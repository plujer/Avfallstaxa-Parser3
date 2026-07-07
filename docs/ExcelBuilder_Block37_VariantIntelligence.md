# Block37 – Variant Intelligence Engine

## Syfte
Block37 identifierar variantdimensioner inom samma taxefamilj. Exempel är volym, fraktion, intervall, kodvariant och fastighetstyp/användning.

## Principer
- Taxa_från_edp är fortsatt facit och ändras inte automatiskt.
- Standardtaxor och variantprofiler är endast beslutsstöd.
- Kommunprojekten hålls separata. Variantkunskap är generell och får inte blanda kommununika EDP-data.

## Output
- `output/excel/variant_intelligence_report.txt`
- `output/excel/variant_profiles.csv`
- `output/excel/variant_intelligence_console.txt`

## Verifiering
Blocket verifieras via `run_project.bat`, som kör hela pipeline, samtliga tester och skapar rapportzip.
