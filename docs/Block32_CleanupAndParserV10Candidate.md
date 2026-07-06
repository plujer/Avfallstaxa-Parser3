# Block 32 – Cleanup + Parser v1.0 Candidate

Detta block stabiliserar körningen efter Block 31.

## Viktigt resultat från senaste rapporten

Acceptance-rapporten visade redan:

```text
6.1.1: 6/6
6.1.2: 103/103
6.1.3: 4/4
6.1.4: 4/4
Totalt: 117/117
```

Parsern är därför en **Parser v1.0-kandidat**.

## Fixar i detta block

- `build_report.bat` skriver direkt till rätt output-undermappar.
- ZIP-filen skapas i `rapportzip/`.
- `tools/organize_output.py` görs om till en ofarlig compatibility-stub.
- Ny `tools/clean_output_root.py` rensar gamla rapportfiler i `output/` innan ny körning.
- Syntaxfelet i `tests/test_rapportzip_structure.py` rättas.
- Output-mappen `output/word/` behålls för framtida Word-generator.

## Kör

```bat
python -m pytest
build_report.bat
```
