# Block39 – Composite Matching Engine

## Syfte

Block39 inför ett samlat matchningslager som väger ihop befintliga beslutsstöd:

dokumentstruktur, hierarkisk kontext, taxefamilj, variant, semantiska attribut,
EDP-träff och standardtaxeförslag.

## Regler

- `Taxa_från_edp` är fortsatt facit och ändras inte automatiskt.
- Standardtaxor används endast som beslutsstöd.
- Kommunprojekten hålls separata; composite matching får inte blanda kommununik data.
- Resultatet är en förklarande poäng och status: `MATCH`, `REVIEW` eller `NO_MATCH`.

## Rapporter

- `output/excel/composite_matching_report.txt`
- `output/excel/composite_matches.csv`
- `output/excel/composite_matching_console.txt`

## Verifiering

Kör `run_project.bat` och skicka senaste rapportzip från `rapportzip\`.
