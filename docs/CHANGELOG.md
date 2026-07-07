# CHANGELOG – Excel Builder

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
