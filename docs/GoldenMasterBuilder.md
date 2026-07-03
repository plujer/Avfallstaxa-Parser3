# Golden Master Builder

Block 6 lägger till funktioner för att skapa, slå ihop och jämföra facit.

## Kommandon

Skapa preliminärt facit från parserresultat:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --build-golden
```

Det skapar:

```text
output/parser_facit_generated.yaml
```

## Viktigt

Det genererade facit är ett utkast. Det manuellt verifierade facit är fortfarande styrande.
