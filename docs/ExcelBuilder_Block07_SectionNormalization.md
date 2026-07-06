# Excel Builder Block 07 – Section Normalization

Detta block rättar första stora matchningshindret.

## Problem

Parsern skriver paragraf som:

```text
2.1
6.1.2
```

medan arbets-Excel ofta har:

```text
§2.1
§6.1.2
```

Det gjorde att Matching Engine fick:

```text
EXACT: 0
PROBABLE: 0
NEW: 241
```

## Lösning

`MatchNormalizer` har nu en särskild `normalize_section()` som tar bort paragraftecknet `§`.

## Kör

```bat
python -m pytest
build_excel_report.bat
```

Skicka senaste ZIP-filen från:

```text
rapportzip/
```
