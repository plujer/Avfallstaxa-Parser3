# Block35 – Hierarchical Context Resolver

## Syfte

Block35 ersätter rullande parserkontext med hierarkisk kontext baserad på Document Structure Engine från Block34.

Målet är att taxarader ska ärva kontext från rätt SECTION/SUBSECTION och att kontext ska nollställas när dokumentet går vidare till ny rubrik eller ny fastighetstyp.

## Viktiga regler

- Taxa_från_edp ändras aldrig.
- Originalparserrader bevaras.
- Struktur-/rubrikrader exporteras inte som taxor.
- Kontext är beslutsstöd och får inte skriva över kommununik EDP-data.
- Kommunprojekten hålls separata.

## Ändring

`ParserContextResolver` kör nu `DocumentStructureEngine` internt och använder strukturträdet för att:

1. identifiera aktiva SECTION/SUBSECTION,
2. ärva fastighetstyp/avfallstyp/tjänstetyp/behållartyp från rätt förälder,
3. nollställa underkontext vid nya syskonrubriker,
4. skriva hierarkisökväg till rapport.

## Nya rapportfält

`output/excel/context_resolved_rows.csv` innehåller nu även:

- `Hierarchy path`
- `Parent structure index`

## Test

Nya regressionstester kontrollerar att:

- fastighetstyp inte läcker från En- och tvåbostadshus till Fritidshus,
- strukturrubriker inte blir taxarader i Context Resolver,
- sektion byts från Slam till Verksamhetsavfall utan gammal kontextläckning.

## BAT-filer

Block35 levereras med standardiserade körfiler:

- `run_project.bat`
- `run_tests.bat`
- `run_reports.bat`
- `run_clean.bat`
- `git_commit_block.bat`
- `git_release_block.bat`

Normal körning är alltid `run_project.bat`.
