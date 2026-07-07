# Excel Builder – START HÄR

## Aktuell status

- Projekt: Excel Builder
- Överlämningsversion: `v0.9.3`
- Senaste stabila punkt: `Block33 – Build System Stabilization`
- Rekommenderad Git-tagg: `v0.9.3-build-stable`
- Datum för överlämning: `2026-07-07`
- Nästa planerade block: `Block34 – Document Structure Engine`

## Syfte

Excel Builder ska ta emot:

```text
1. Word-dokument med taxetext
2. Kommununik EDP-export
3. Versionsstyrd masterarbetsbok
```

och skapa:

```text
1. Kommununik färdig Excel-arbetsbok
2. Beslutsrapporter
3. Förslag på saknade taxor
4. Underlag för framtida EDP-export/import
```

## Viktigaste reglerna

```text
Taxa_från_edp är alltid facit.
Befintliga EDP-taxor får aldrig ändras automatiskt.
Standardtaxor är endast beslutsstöd och förslag.
Kommunprojekten Sorsele, Malå och Norsjö får aldrig blandas.
Masterarbetsboken får inte ändras utan godkänd versionshantering.
Kunskap delas – kommununik data delas inte.
```

## Börja i ny ChatGPT-konversation

Ladda upp:

```text
1. ExcelBuilder_Project_Handover_v0.9.3.zip
2. Senaste rapport-ZIP från rapportzip/
3. Senaste masterarbetsbok om den ändrats
```

Kopiera sedan texten i:

```text
docs/NEXT_SESSION_PROMPT.md
```

## Lokal kontroll

Kör i projektmappen:

```bat
git status
```

```bat
python tools\check_v1_spec.py
```

```bat
python -m pytest
```

```bat
build_excel_report.bat
```
