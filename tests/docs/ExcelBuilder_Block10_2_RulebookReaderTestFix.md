# Excel Builder Block 10.2 – Rulebook Reader Test Fix

Detta block rättar endast det sista röda testet från föregående rapport.

## Problem

`test_rulebook_reader_reads_rule_sheets` skapade inte en komplett testarbetsbok för de regler som `EdpRuleValidator` förväntar sig.

Det gav ett falskt testfel trots att den riktiga arbetsboken lästes korrekt.

## Lösning

Testet skapar nu en temporär arbetsbok med minsta nödvändiga regelmaterial:

- `strTaxekod`
- `strTaxebenamning`
- `strTaxedelAvser`
- `strFaktor`
- `strFormel`
- `Taxa_från_edp`
- `Taxa_Saknas`
- `Aktuellt pris`
- `får aldrig redigeras manuellt`

## Ingen produktionslogik ändras

Detta block ändrar endast:

```text
tests/test_rulebook_reader.py
```

## Kör tester

```bat
python -m pytest
```

## Bygg rapportpaket

```bat
build_excel_report.bat
```

## Skicka tillbaka

```text
rapportzip/
```
