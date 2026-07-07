# Block40 – Explainable Decision Engine

## Syfte
Block40 lägger till ett förklaringslager ovanpå Composite Matching Engine. Varje beslut får en spårbar `DecisionTrace` med totalpoäng, confidence, viktigaste signaler och eventuell orsak till att raden kräver granskning eller avvisas.

## Regler
- `Taxa_från_edp` ändras inte automatiskt.
- Standardtaxor används endast som beslutsstöd.
- Kommununik data hålls separerad.
- Förklaringar ska vara beslutsunderlag, inte automatisk ändring av facit.

## Rapporter
Blocket skapar:

- `output/excel/explainable_decision_report.txt`
- `output/excel/decision_traces.csv`
- `output/excel/explainable_decision_console.txt`

## BAT-filer
Kör normalt `run_project.bat`. Vid fel körs `run_tests.bat`. Efter godkännande körs `git_commit_block.bat`.
