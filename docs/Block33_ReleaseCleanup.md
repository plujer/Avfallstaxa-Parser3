# Block 33 – Release Cleanup

Detta block gör inga ändringar i parserlogiken.

## Syfte

Rätta föråldrade tester inför den riktiga `v1.0.0`-releasen.

## Fixar

- `tests/test_acceptance_debugger.py` antar inte längre att första facitsektionen är §6.1.2.
- Testerna söker upp rätt sektion via sektionsnummer.
- `tests/test_output_structure_files.py` verifierar den nya `rapportzip/`-strukturen.
- Gamla förväntningar på `docs-mappen` tas bort.

## Mål

Efter detta block ska körningen visa:

```text
Acceptance: 117/117
pytest: 0 failed
```

## Kör

```bat
python -m pytest
build_report.bat
```

ZIP-filen för återrapportering finns därefter i:

```text
rapportzip/
```
