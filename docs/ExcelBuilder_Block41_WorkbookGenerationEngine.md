# Block41 – Workbook Generation Engine

Workbook Generation Engine skriver spårbara beslutsresultat till den genererade Arbets-Excel-filen.

## Ingår

- `Decision_Trace` – full beslutsspårning från Explainable Decision Engine.
- `Workbook_Generation` – sammanfattning av skrivningen till arbetsboken.
- Nya kolumner i `Taxepunkter`:
  - Beslutsspår kandidat
  - Beslutsspår status
  - Beslutsspår säkerhet
  - Beslutsspår motivering

## Viktiga regler

- `Taxa_från_edp` är facit och ändras inte automatiskt.
- Beslutsspårning är endast beslutsstöd.
- Kommunprojekt hålls separata.
