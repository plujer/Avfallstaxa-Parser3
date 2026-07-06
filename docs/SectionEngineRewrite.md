# Block 8 – Section Engine Rewrite

Detta block rättar felet där parsern tolkade `2026` som sektion.

## Viktiga regler

Acceptera:

- `2 § Grundavgift`
- `2.5.1 § Budning`
- `6.1.2 § Hanteringsavgifter`

Avvisa:

- `2026`
- `2026-03-13`
- `170601*`
- `200301`
- `3295`
- prisrader
- taxarader utan paragraftecken

## Test

```bat
python -m pytest
```

## Semantisk kontroll

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Förväntat: section summary ska inte längre visa `2026`.
