# Excel Builder Block 10.3 – Repository Cleanup

Detta block rättar testinsamlingsfelet:

```text
import file mismatch:
tests/test_rulebook_reader.py
tests/tests/test_rulebook_reader.py
```

## Orsak

Det finns en felaktig extra testkatalog:

```text
tests/tests/
```

Den kan uppstå om en ZIP packas upp på fel nivå.

## Lösning

Ny cleanup:

```text
tools/cleanup_duplicate_tests.py
```

Den tar bort:

```text
tests/tests/
```

och rapporterar eventuella dubbla testfilnamn.

`build_excel_report.bat` kör cleanup före pytest.

## Kör cleanup manuellt

```bat
python tools\cleanup_duplicate_tests.py
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
