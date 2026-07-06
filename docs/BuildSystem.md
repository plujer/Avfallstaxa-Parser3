# Block 15 – Build System

Detta block gör att du kan skapa en komplett rapport-ZIP utan skärmbilder.

## Kör

Dubbelklicka på:

```text
build_report.bat
```

eller kör:

```bat
build_report.bat
```

Det skapar en ZIP i:

```text
output\Parser3_Run_YYYY-MM-DD_HH-mm-ss.zip
```

## Innehåll i ZIP

- parser3_result.json
- parser3_report.txt
- parser3_precision_report.txt
- parser3_explain_report.txt
- parser3_architecture_report.txt
- pytest_report.txt
- parser_console.txt
- environment_report.txt

## Viktigt

`pytest.ini` och `tests/conftest.py` gör att `parser3` hittas korrekt av pytest.
