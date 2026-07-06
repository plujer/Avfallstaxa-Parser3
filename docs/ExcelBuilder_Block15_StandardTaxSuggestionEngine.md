# Excel Builder Block 15 – Standard Tax Suggestion Engine

Detta block börjar använda standardtaxorna som beslutsstöd.

## Syfte

När en taxa finns i Word men saknar säker kommun-EDP-match ska systemet kunna söka i standardtaxorna och föreslå en möjlig taxekod.

## Viktigt

Förslag från standardtaxor är **inte** bekräftade EDP-koder.

De ska senare skrivas till:

```text
Taxa_Förslag
Regelspårning
```

och granskas innan import.

## Nya delar

- `StandardTaxReader`
- `StandardTaxSuggestionEngine`
- `StandardTaxSuggestionReporter`
- `excel_builder_standard_suggestions.py`

## Nya rapporter

```text
output/excel/standard_tax_suggestions_report.txt
output/excel/standard_tax_suggestions.csv
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
