# Excel Builder Block 28 – Semantic Candidate Ranking

Detta block ersätter exakt nyckelgruppering med poängbaserad kandidat-ranking.

## Syfte

Word-profiler jämförs mot kandidater från:

- standardtaxor,
- Rule Repository / Taxepunkter,
- Rule Repository / EDP.

Varje kandidat får:

- score,
- status,
- förklaring.

## Statusnivåer

```text
EDP_MATCH
STANDARD_PROPOSAL
RULE_PROPOSAL
REVIEW_REQUIRED
LOW_CONFIDENCE
```

## Nya rapporter

```text
output/excel/semantic_candidate_report.txt
output/excel/semantic_candidates.csv
```

## Viktigt

Detta ändrar inte `Taxa_från_edp`.

Det är beslutsunderlag för nästa steg där Decision Engine ska använda topprankade kandidater.

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
