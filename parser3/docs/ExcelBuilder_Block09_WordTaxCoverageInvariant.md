# Excel Builder Block 09 – Word Tax Coverage Invariant

Detta block lägger in ett absolut krav i Excel Builder:

> Alla taxor som parsern hittar i Word-dokumentet måste finnas som egen rad i `Taxepunkter`.

Det gäller oavsett om:

- `Taxa_från_edp` är tom,
- EDP-kod saknas,
- EDP-matchning är osäker,
- pris saknas.

EDP får komplettera en rad, men får aldrig avgöra om en Word-taxa ska finnas som rad.

## Nya delar

- `WordTaxCoverageValidator`
- `CoverageReporter`
- `excel_builder_coverage.py`

## Nya rapporter

```text
output/excel/word_tax_coverage_report.txt
output/excel/word_tax_coverage_results.csv
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
