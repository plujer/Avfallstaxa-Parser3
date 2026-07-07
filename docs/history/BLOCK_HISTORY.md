# BLOCK_HISTORY – Excel Builder

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

## Block43 – Master Source Integration & Immutable Template Guard

Syfte: Göra de nya masterfilerna till projektets officiella källor och införa tekniska skydd så att de aldrig skrivs över.

Ändringar:
- `Taxestruktur_Master_v1.0.docx` och `ArbetsExcel_Template_v1.0.xlsx` lades in som officiella masterfiler.
- Ny konfiguration `config/master_sources.json`.
- Ny `ImmutableMasterGuard`.
- `TemplateMasterManager` och `WorkbookWriter` uppdaterades för masterkopiering.
- BAT-filer uppdaterades för standardiserad körning.

Regel: Om master behöver ändras ska ny versionsfil skapas. Befintlig master ändras aldrig.

## Block44 - Immutable Master Enforcement

Syfte: Göra masterfilskyddet tekniskt och testbart.

Regler:
- Word-master och Excel-master får aldrig skrivas över.
- Ändringsbehov hanteras genom ny versionsfil.
- `Taxepunkter!A:E` är mallområde och skrivskyddat.
- `Taxa_från_edp` är facit och skrivskyddat.

Leverans:
- Guard-moduler
- Testfall
- Verifieringsverktyg
- Uppdaterade BAT-filer
