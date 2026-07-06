# Excel Builder Block 08 – Rulebook Reader

Detta block bygger den regelbas som Excel Builder ska följa innan matchningslogiken utökas.

## Varför

Arbetsboken innehåller redan regler för hur taxekoder och EDP-data ska användas. Vi ska därför inte gissa matchningsregler.

## Nya delar

- `RulebookReader`
- `EdpRuleValidator`
- `RulebookReporter`
- `excel_builder_rulebook.py`

## Ny rapport

```text
output/excel/edp_rulebook_report.txt
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
