# PROJECT_RULES – Excel Builder

## Regler som aldrig får brytas

```text
Taxa_från_edp är alltid facit.
Taxa_från_edp får inte ändras automatiskt.
Standardtaxor är endast förslag.
Kommunprojekt får aldrig blandas.
Masterarbetsboken får inte ändras direkt.
Masterändringar kräver godkännande.
Alla block ska ha tester.
Alla block ska skapa rapportzip.
Kunskap delas – data delas inte.
```

## Kommunisolering

```text
Sorsele använder endast Sorseles EDP-export.
Malå använder endast Malås EDP-export.
Norsjö använder endast Norsjös EDP-export.
```

## Beslut

```text
Rubriker ska inte bli NEW_TAXA.
Osäkra kandidater ska bli REVIEW_REQUIRED.
Toppkandidater nära varandra ska bli REVIEW_REQUIRED.
Alla beslut ska ha confidence och motivering.
```

## Master

```text
Master kopieras före skrivning.
Ny masterversion skapas endast efter godkännande.
Versionshistorik ska uppdateras vid masterändring.
```

## Block43 – Immutable Master Source Policy

Följande filer är projektets officiella masterkällor från och med v1.0:

- `data/word_templates/Taxestruktur_Master_v1.0.docx`
- `data/master_templates/ArbetsExcel_Template_v1.0.xlsx`

Regler:

1. Masterfiler är immutable och får aldrig skrivas över.
2. Word-mastern får endast läsas av parsern.
3. Excel-mastern får endast kopieras till arbetskopior.
4. Om redigering krävs ska en ny versionsfil skapas, exempelvis `v1.1`.
5. Fliken `Taxepunkter` kolumn A:E får inte skrivas automatiskt.
6. Fliken `Taxa_från_edp` är facit och får inte skrivas automatiskt i någon kolumn eller rad.
7. Projektet ska hämta aktiva masterkällor från `config/master_sources.json`.

## Block44 - Immutable Master Enforcement

Masterfiler är immutable. Projektet får aldrig skriva till eller spara över:

- `data/word_templates/Taxestruktur_Master_v1.0.docx`
- `data/master_templates/ArbetsExcel_Template_v1.0.xlsx`

Om en master behöver ändras ska en ny versionsfil skapas. Tidigare masterversioner lämnas orörda.

Skyddade arbetsboksområden:

- `Taxepunkter!A:E` får inte skrivas automatiskt.
- `Taxa_från_edp` får inte skrivas automatiskt i någon cell.

All generering ska ske via arbetskopior i `output/` eller kommunseparerade projektmappar.
