# PROJECT_STATUS – Excel Builder

## Senaste stabila version

```text
v0.9.4-block35-candidate
Block35 – Hierarchical Context Resolver
```

## Senaste verifierade rapport

```text
ExcelBuilder_Run_2026-07-07_10-37-44.zip
```

## Aktuell sammanfattning

Projektet har lämnat grundläggande infrastrukturfelsökning och är nu i domänintelligensfasen.

Det som fungerar:

```text
Parser
Excel Builder
Masterkopiering
Kommunisolering
EDP-import
Standardtaxekatalog
Workbook Schema Scanner
Dynamic Taxepunkter Reader
Rule Repository
Semantic Profiles
Semantic Candidate Ranking
Semantic Decision Engine
Context Resolver
Tax Code Intelligence
Full build pipeline
v1.0-specifikation
```

## Senaste viktiga resultat

Block33 återställde den fullständiga byggkedjan efter att Block32 av misstag hade ersatt den med en minimal specifikationspipeline.

Nu gäller:

```text
v1.0-specifikationskontroll körs först
full rapportpipeline körs igen
alla centrala rapporter ingår i rapportzip
stabiliseringstester finns för att förhindra regression
```

## Känd huvudflaskhals

Parsern och Context Resolver behandlar fortfarande vissa rubriker som taxor.

Exempel på rader som inte ska bli `NEW_TAXA`:

```text
En- och tvåbostadshus
Fritidshus
Verksamhet
Lägenhet i flerbostadshus
```

Dessa är dokumentstruktur/rubriker, inte faktiska taxepunkter.

## Senaste genomförda block

```text
Block35 – Hierarchical Context Resolver
```

Resultat:

```text
1. Context Resolver använder Document Structure Engine internt.
2. Strukturrubriker skickas inte ut som kontextlösta taxarader.
3. Fastighetstyp, avfallstyp, tjänstetyp och behållartyp ärvs från aktiv hierarki.
4. Underkontext nollställs vid nya syskonrubriker så kontext inte läcker mellan avsnitt.
5. context_resolved_rows.csv innehåller Hierarchy path och Parent structure index.
6. Standardiserade BAT-filer införs för körning, tester, rapporter och Git-steg.
```

## Nästa prioritet

```text
Block36 – Tax Family Intelligence
```

## Aktuell mognadsbedömning

| Område | Status |
|---|---:|
| Projektarkitektur | 99 % |
| Excel-/EDP-hantering | 99 % |
| Projektisolering | 100 % |
| Standardtaxekatalog | 99 % |
| Rule Repository | 95 % |
| Semantisk modell | 94 % |
| Tax Code Intelligence | 85 % |
| Beslutsmotor | 88 % |
| Dokumentstrukturförståelse | 82 % |

## Aktuellt block

Block36 – Tax Family Intelligence är levererat för verifiering.

Fokus:
- gruppera taxekoder i stabila familjer,
- förbättra semantisk kandidatrankning med taxefamiljsbonus,
- lägga till taxefamiljsrapporter i rapportzip,
- bibehålla regeln att Taxa_från_edp är facit.
