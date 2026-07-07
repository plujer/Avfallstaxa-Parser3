# ExcelBuilder Block34 – Document Structure Engine

## Syfte

Block34 inför ett icke-destruktivt dokumentstrukturlager mellan parsern och semantik/beslut.
Målet är att skilja dokumentrubriker, mellanrubriker, tabellrubriker, tabellrader och verkliga taxepunkter.

## Resultat

Ny klassificering:

```text
SECTION
SUBSECTION
TABLE_HEADER
TABLE_ROW
TAX_NODE
NOTE
```

Endast `TAX_NODE` skickas vidare till kontextlösning, Tax Knowledge, semantiska profiler, kandidat-ranking och beslutsmotorerna.

## Viktig regression som löses

Följande rader klassas nu som `SUBSECTION` och skickas inte vidare som taxor:

```text
En- och tvåbostadshus
Fritidshus
Verksamhet
Lägenhet i flerbostadshus
```

De ska alltså inte kunna bli `NEW_TAXA` i beslutsrapporten.

## Ändrade/nya filer

```text
excel_builder/models/document_structure_models.py
excel_builder/document/__init__.py
excel_builder/document/document_structure_engine.py
excel_builder/reports/document_structure_reporter.py
excel_builder_document_structure.py
tests/test_document_structure_engine.py
```

Uppdaterade integrationsfiler:

```text
excel_builder_context_resolve.py
excel_builder_tax_knowledge.py
excel_builder_semantic_profiles.py
excel_builder_semantic_candidates.py
excel_builder_decide.py
excel_builder_decide_semantic.py
build_excel_report.bat
tools/zip_excel_report.ps1
excel_builder/models/__init__.py
excel_builder/reports/__init__.py
```

## Master

Rapportbygget använder nu versionsstyrd master:

```text
data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx
```

Den skrivs inte över av Block34.

## Testresultat

Lokal verifiering:

```text
python tools/check_v1_spec.py
python -m pytest -q
```

Resultat:

```text
v1.0 specification validation passed.
291 passed
```

Dokumentstruktur på aktuell parserrapport:

```text
Rows: 241
TAX_NODE: 229
SUBSECTION: 8
SECTION: 4
TABLE_HEADER: 0
NOTE: 0
```

Semantisk beslutsmotor efter filtrering:

```text
Parser rows: 229
Context enriched rows: 229
Semantic candidates: 2290
REVIEW_REQUIRED: 130
NEW_TAXA: 99
```
