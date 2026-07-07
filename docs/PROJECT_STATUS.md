# PROJECT_STATUS

Aktuellt block: Block47 – Word Excel Mapping Engine.

Status: Paket framtaget och verifierat lokalt.

Verifiering:
- `python -m pytest -q`
- Resultat: 350 passed

Viktig ändring:
- `run_project.bat` kör fortsatt hela kedjan.
- I slutet skapas även ett aktuellt kompakt projektpaket i `project_packages/Project_For_ChatGPT.zip`.
- Word → Excel-mappning rapporteras i `word_excel_mapping_report.txt` och `word_excel_mapping.csv`.

Permanenta regler:
- Word-master ändras aldrig.
- Excel-master ändras aldrig.
- `Taxepunkter` A:E ändras aldrig automatiskt.
- `Taxa_från_edp` ändras aldrig.
- Samma EDP-taxa får användas av flera Word-rader utan att det automatiskt är fel.
