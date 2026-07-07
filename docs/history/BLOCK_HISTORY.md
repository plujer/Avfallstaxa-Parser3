# BLOCK_HISTORY – Excel Builder


## Block35 – Hierarchical Context Resolver

Införde hierarkisk kontext baserad på Document Structure Engine. Kontext ärvs nu från rätt SECTION/SUBSECTION och nollställs vid nya syskonrubriker, vilket minskar risken att exempelvis En- och tvåbostadshus påverkar Fritidshus eller att Slam-kontext följer med in i Verksamhetsavfall.

## Block34 – Document Structure Engine

Införde ett dokumentstrukturlager som skiljer rubriker och struktur från verkliga taxepunkter. Endast TAX_NODE skickas vidare till semantik och beslutsmotor. Detta stoppar kända rubriker som En- och tvåbostadshus, Fritidshus, Verksamhet och Lägenhet i flerbostadshus från att bli NEW_TAXA.

## Block33 – Build System Stabilization

Återställde full rapportpipeline och la till v1.0-kontroll som första steg.

## Block32 – v1.0 Specification

Skapade specifikation, roadmap och invariants.

## Block31 – Tax Code Intelligence

Tolkar EDP-taxekoder till semantiska delar.

## Block30 – Context Resolver

Berikar parserrader med kontext.

## Block29 – Semantic Decision Integration

Kopplar semantisk kandidatranking till beslut.

## Block28 – Semantic Candidate Ranking

Poängbaserad kandidatmatchning.

## Block27 – Tax Semantic Profile Engine

Gemensam profil för taxor från olika källor.

## Block26 – Standard Tax Catalog Reverse Engineering

Läser standardtaxefilen med flera sektioner.

## Block25 – Dynamic Taxepunkter Reader

Läser Taxepunkter från dynamiskt hittad rubrikrad.

## Block24 – Workbook Schema Scanner

Scannar masterarbetsbokens struktur.

## Block23 – Master Rule Repository

Bygger regelrepository från master.

## Block22 – Knowledge Index

Första kunskapsindexet.

## Block21 – Knowledge Based Standard Matching

Kunskapsbaserad standardmatchning.

## Block1–20

Grundläggande parser, Excel Builder, teststruktur, rapportpaket, standardtaxestöd, projektisolering och stabilisering.

## Block36 – Tax Family Intelligence

Status: Levererad för verifiering.

Syfte: Förstå relationen mellan taxekoder inom samma familj, till exempel `KÄ240RM26`, `KÄ240RM52` och `KÄ240RMFV`.

Verifiering:

- `run_project.bat`
- `run_tests.bat` endast vid felsökning
- rapportzip skickas tillbaka till granskning

Regel: Informationen används endast som beslutsstöd. `Taxa_från_edp` ändras inte automatiskt.


## Block37 – Variant Intelligence Engine
Variantdimensioner inom taxefamiljer identifieras som beslutsstöd: volym, fraktion, intervall, variant och användningstyp.

## Block38 – Semantic Attribute Intelligence

Syfte: skapa ett konservativt attributlager ovanpå taxefamiljer och varianter.

Ändringar:
- Nytt paket `excel_builder/semantic_attributes/`.
- Ny modellfil `semantic_attribute_models.py`.
- Ny CLI `excel_builder_semantic_attributes.py`.
- Ny reporter `semantic_attribute_reporter.py`.
- Build-pipeline kör attributsteget innan befintlig taxekunskap och semantisk kandidatrankning.

Verifiering: hela testsviten ska köras via `run_project.bat` och rapportzip ska skickas tillbaka.

## Block39 – Composite Matching Engine

Composite Matching Engine samlar tidigare intelligenslager till en förklarande matchpoäng:

- EDP exact match
- Tax Family Intelligence
- Variant Intelligence
- Semantic Attribute Intelligence
- Hierarchical Context
- Document Structure

Nya rapportfiler:

- `composite_matching_report.txt`
- `composite_matches.csv`

BAT-filerna är uppdaterade för Block39.
## Block40 – Explainable Decision Engine
Införde ett förklaringslager ovanpå Composite Matching Engine. Besluten får confidence, primära orsaker och signalsammanställning utan att ändra Taxa_från_edp.

## Block41 – Workbook Generation Engine

Syfte: göra slutprodukten mer spårbar genom att skriva Explainable Decision Engine-resultat till själva arbetsboken.

Ändringar:
- Nytt paket `excel_builder/workbook_generation/`.
- Ny modellfil `workbook_generation_models.py`.
- Ny CLI `excel_builder_workbook_generation.py`.
- Ny reporter `workbook_generation_reporter.py`.
- Build-pipeline kör Workbook Generation Engine efter semantisk beslutsmotor och före täckningskontroll.

Verifiering: kör `run_project.bat`; `run_tests.bat` används endast om huvudkörningen själv säger att tester behövs.

Regel: `Taxa_från_edp` ändras inte. Beslutsspårning är endast beslutsstöd.
