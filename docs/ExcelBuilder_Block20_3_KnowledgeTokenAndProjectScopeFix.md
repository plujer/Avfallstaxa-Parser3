# Excel Builder Block 20.3 – Knowledge Token and Project Scope Fix

Detta block rättar de tre kvarvarande felen från rapporten.

## Fix 1 – Tax Knowledge tokenmatchning

`TaxKnowledgeExtractor` matchade tidigare delsträngar. Det gjorde att `trä` kunde matcha inne i ordet `extra`.

Nu används tokenbaserad matchning.

## Fix 2 – Projekttester

Huvudrapporten är nu anpassad till primär körning:

```text
Sorsele
```

Malå och Norsjö finns kvar i:

```text
build_all_projects.bat
```

men behöver inte byggas i varje huvudrapport.

## Kontrollera testsyntax

```bat
python tools\check_test_syntax.py
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
