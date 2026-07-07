# Excel Builder v1.0 – låst arbetsspecifikation

## Syfte

Excel Builder ska kunna ta emot:

```text
1. Ett Word-dokument med taxetext
2. En EDP-export
3. En versionsstyrd masterarbetsbok
```

och skapa:

```text
1. En färdig kommununik Excel-arbetsbok
2. Beslutsrapporter
3. Förslag på saknade taxor
4. Underlag för ny EDP-export
```

## Grundprinciper

### 1. Kommunens EDP är facit

`Taxa_från_edp` är alltid fast indata.

Systemet får:

```text
läsa
jämföra
rapportera
föreslå
```

Systemet får inte:

```text
ändra befintlig EDP-taxa automatiskt
skriva över kommunens EDP-kod
blanda EDP-exporter mellan kommuner
```

### 2. Standardtaxor är bara förslag

Standardtaxekatalogen är global kunskap.

Den får användas för:

```text
förslag
jämförelse
kontroll
saknade taxor
```

Den får inte användas för att ersätta en befintlig kommun-EDP utan manuell granskning.

### 3. Masterarbetsboken är både regelbok och mall

Masterarbetsboken används som:

```text
visuell Excel-mall
regelkälla
formelkälla
referensstruktur
```

Generatorn ska alltid:

```text
kopiera master
fylla kopian
spara output
```

Den ska aldrig skriva direkt i master.

### 4. Masterändringar kräver godkännande

Om ny flik, kolumn, rad eller formel behövs i master ska systemet:

```text
1. föreslå ändringen
2. invänta godkännande
3. skapa ny versionsbaserad master
4. dokumentera ändringen
```

Exempel:

```text
data/master_templates/ArbetsExcel_Template_v0.2.0_draft.xlsx
data/master_templates/ArbetsExcel_Template_v1.0.0_locked.xlsx
```

### 5. Kunskap delas – data delas inte

Generell kunskap får delas:

```text
taxekodstolkningar
taxefamiljer
semantiska regler
standardtaxelogik
inlärda generella samband
```

Kommununik data får inte delas:

```text
EDP-exporter
kommununika arbetsböcker
kommununika beslut
kommununika taxor
```

## Mappstruktur

```text
data/
    master_templates/
        ArbetsExcel_Template_vX.Y.Z_status.xlsx
        VERSION_HISTORY.md

    edp_standard/
        EDP_Future_Standard_Taxor_Renhallning.xlsx

    edp_exports/
        Sorsele.xlsx
        Mala.xlsx
        Norsjo.xlsx

    knowledge/
        v1/
            tax_code_patterns.csv
            tax_families.csv
            learned_rules.csv
            semantic_patterns.csv

    projects/
        Sorsele/
            project_config.json
        Mala/
            project_config.json
        Norsjo/
            project_config.json

output/
    excel/
    projects/
        Sorsele/
        Mala/
        Norsjo/
    diagnostics/
    reports/
    archive/

rapportzip/
```

## Körflöde v1.0

```text
Word
  ↓
Parser
  ↓
Document Structure Engine
  ↓
Tax Node Extractor
  ↓
Context Resolver
  ↓
Tax Semantic Profile Engine
  ↓
Semantic Candidate Ranking
  ↓
Semantic Decision Engine
  ↓
Excel Builder
  ↓
Kommununik färdig arbetsbok
  ↓
EDP Export Builder
```

## Obligatoriska moduler

### Parser

Ska extrahera taxepunkter från Word.

### Document Structure Engine

Ska skilja på:

```text
rubrik
grupp
taxerad
tabellrubrik
tabellrad
förklarande text
```

Endast verkliga taxerader ska skickas vidare till slutlig matchning.

### Context Resolver

Ska ärva kontext inom rätt dokumentgren.

Kontext får inte läcka mellan oberoende avsnitt.

### Tax Code Intelligence

Ska tolka EDP-taxekoder.

Exempel:

```text
KÄ240RM26FV
```

ska ge:

```text
prefix = KÄ
container_type = Kärl
volume = 240
waste_code = RM
interval = 26
variant = FV
family_key = KÄ240RM
```

### Tax Family Intelligence

Ska gruppera taxor i familjer.

Exempel:

```text
KÄ240RM
    26
    52
    104
    FV
    FRI
```

### Rule Repository

Ska byggas från masterarbetsboken och innehålla:

```text
Taxepunkter
Taxa_från_edp
dokumentationsblad
standardreferenser
manuella regler
```

### Semantic Candidate Ranking

Ska jämföra Word-taxor mot kandidater från:

```text
kommunens EDP
Taxepunkter
standardtaxor
regelrepository
taxefamiljer
```

### Semantic Decision Engine

Ska fatta beslut baserat på rankade kandidater.

Beslutsstatus:

```text
EDP_MATCH
STANDARD_PROPOSAL
RULE_PROPOSAL
REVIEW_REQUIRED
NEW_TAXA
NOT_A_TAXA
```

### Rule Learning

När användaren manuellt rättar ett förslag ska systemet kunna skapa generell kunskap utan att blanda kommunprojekt.

## Obligatoriska rapporter

Varje körning ska skapa:

```text
pytest_report.txt
test_syntax_report.txt
workbook_schema_report.txt
standard_catalog_schema_report.txt
tax_code_intelligence_report.txt
context_resolution_report.txt
document_structure_report.txt
tax_family_report.txt
semantic_profile_report.txt
semantic_candidate_report.txt
tax_decision_semantic_report.txt
word_tax_coverage_report.txt
master_rule_repository_report.txt
excel_report_manifest.txt
```

## Obligatoriska Excel-output

Varje kommunprojekt ska skapa:

```text
ArbetsExcel_<Kommun>_byggd.xlsx
```

Arbetsboken ska bygga på masterkopia och bevara:

```text
utseende
formler
tabeller
datavalidering
villkorlig formatering
pivottabeller
namngivna områden
kolumnbredder
dolda blad
utskriftsinställningar
```

## Beslutsregler

### Prioritet

```text
1. Befintlig kommun-EDP
2. Taxepunkter med taxekod
3. Standardtaxor
4. Taxepunkter utan taxekod
5. Dokumentationsregler
```

### Ambiguitet

Om två toppkandidater ligger för nära varandra ska beslutet bli:

```text
REVIEW_REQUIRED
```

### Rubriker

Rubriker ska inte bli:

```text
NEW_TAXA
```

De ska klassas som:

```text
NOT_A_TAXA
```

## v1.0 acceptanskriterier

Version 1.0 kan låsas när:

```text
1. Alla tester passerar.
2. Masterarbetsboken kopieras och ändras inte direkt.
3. Taxepunkter läses från rätt rubrikrad dynamiskt.
4. Standardtaxekatalogen läses med flera sektioner.
5. Taxekoder tolkas till familjer.
6. Rubriker separeras från taxor.
7. Alla Word-taxor finns i Taxepunkter.
8. Kommunprojekt hålls isolerade.
9. Befintliga EDP-taxor ändras inte automatiskt.
10. Beslut har motivering och confidence.
11. Rapportpaket skapas automatiskt.
```
