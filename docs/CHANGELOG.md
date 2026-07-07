# CHANGELOG – Excel Builder


## Block35 – Hierarchical Context Resolver

- Ersatte rullande kontext med hierarkisk kontext baserad på Document Structure Engine.
- Context Resolver klassificerar nu parserrader internt och returnerar endast TAX_NODE/TABLE_ROW.
- Nollställer underkontext vid ny SECTION/SUBSECTION för att förhindra kontextläckning mellan syskonrubriker.
- Lägger till `Hierarchy path` och `Parent structure index` i `context_resolved_rows.csv`.
- Uppdaterade regressionstester för ny förväntad Block35-semantik.
- Införde standardiserade BAT-filer för blockkörning, tester, rapportzip och Git-steg.

## Block34 – Document Structure Engine

- Införde Document Structure Engine.
- Klassificerar parserrader som SECTION, SUBSECTION, TABLE_HEADER, TABLE_ROW, TAX_NODE eller NOTE.
- Filtrerar så att endast TAX_NODE går vidare till kontext, Tax Knowledge, semantik och beslut.
- Förhindrar att kända rubriker/fastighetstyper blir NEW_TAXA.
- La till document_structure_report.txt och document_structure_rows.csv i rapportpaketet.
- Uppdaterade rapportbygget till versionsstyrd master `data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx`.
- La till regressionstester för dokumentstruktur.

## Block33 – Build System Stabilization

- Återställde full `build_excel_report.bat`.
- La till `tools/check_v1_spec.py` som första steg.
- Återställde full rapportzip.
- La till tester som förhindrar att buildkedjan ersätts med minimal pipeline igen.

## Block32 – Version 1.0 Specification

- Skapade v1.0-specifikation.
- Skapade roadmap.
- Skapade invariants.
- Introducerade specifikationskontroll.
- Problem: buildfilen blev för minimal och behövde återställas i Block33.

## Block31 – Tax Code Intelligence

- Införde `TaxCodeParser`.
- Delade upp taxekoder som `KÄ240RM26FV`.
- Skapade rapporter för taxekoder och familjenycklar.

## Block30 – Context Resolver

- Införde `ParserContextResolver`.
- Berikar parserrader med sektion, fastighetstyp, avfallstyp, tjänstetyp och behållartyp.
- Känd brist: rullande kontext kan läcka mellan avsnitt.

## Block29 – Semantic Decision Integration

- Kopplade semantisk kandidatranking till beslutsmotor.
- Införde källprioritet.
- Införde ambiguitetshantering.

## Block28 – Semantic Candidate Ranking

- Införde poängbaserad kandidatjämförelse.
- Skapade förklaringar för kandidatmatchning.

## Block27 – Tax Semantic Profile Engine

- Införde gemensam taxaprofil för Word, standardtaxor och regelrepository.

## Block26 – Standard Tax Catalog Reverse Engineering

- Läste standardtaxefilen med flera sektioner.
- Normaliserade standardtaxor till ny rapportarbetsbok.

## Block25 – Dynamic Taxepunkter Reader

- Löste att `Taxepunkter` har rubrikrad 5.
- Rule Repository började läsa Taxepunkter korrekt.

## Block24 – Workbook Schema Scanner

- Scannade masterarbetsboken.
- Identifierade rubrikrader, tabeller, namngivna områden, formler och struktur.

## Block23 – Master Rule Repository

- Byggde regelrepository från masterarbetsboken.

## Block22 – Knowledge Index

- Införde första indexeringen av Word-taxor och standardtaxor.

## Block21 – Knowledge Based Standard Matching

- Började använda Tax Knowledge i standardmatchning.

## Tidigare block

Tidigare block byggde parser, Excel Builder, rapportkedja, standardtaxestöd, projektisolering och grundläggande testsvit.

## Block36 – Tax Family Intelligence

- Infört taxefamiljsmodell för att gruppera taxekoder efter prefix, volym och avfallstyp.
- Lagt till taxefamiljsparser, repository och matcher.
- Lagt till rapporter för taxefamiljer i rapportzip.
- Lagt till liten taxefamiljsbonus i semantisk kandidatrankning som beslutsstöd.
- Uppdaterat standardiserade BAT-filer för Block36.


## Block37 – Variant Intelligence Engine
- Lade till VariantParser, VariantMatcher och VariantRepository.
- Lade till CLI `excel_builder_variant_intelligence.py`.
- Lade till rapporterna `variant_intelligence_report.txt` och `variant_profiles.csv`.
- Uppdaterade BAT-flödet för Block37.
