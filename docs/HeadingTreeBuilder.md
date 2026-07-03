# Heading Tree Builder

Block 2 lägger till rubrikhierarki.

Parsern kan nu känna igen:

- `2 §`
- `2.2 §`
- `2.2.4 §`
- `6.1.2 §`

## Körning

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --headings
```

## Viktig regel

Rubriker är inte taxor. Rubriker används för att placera taxarader i rätt paragraf.
