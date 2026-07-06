# Excel Builder Block 06 – Report Package Standard

Detta block standardiserar vilka filer som alltid ska skickas tillbaka efter varje Excel Builder-block.

## Kör alltid

```bat
build_excel_report.bat
```

## ZIP skapas i

```text
rapportzip/
```

## ZIP innehåller

- `ArbetsExcel_byggd_fran_parser.xlsx`
- `excel_matching_results.csv`
- `excel_matching_report.txt`
- `excel_matching_console.txt`
- `arbets_excel_profile_report.txt`
- `arbets_excel_snapshot.txt`
- `excel_builder_report.txt`
- `excel_builder_console.txt`
- `excel_inspect_console.txt`
- `pytest_report.txt`
- `parser3_result.json`
- `parser3_acceptance_report.txt`
- `excel_report_manifest.txt`

## Varför

Du ska inte behöva gissa vilka filer jag vill ha. Skicka alltid senaste ZIP-filen från `rapportzip/`.
