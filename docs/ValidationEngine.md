# Validation Engine

Block 5 lägger till validering och första Golden Master.

## Körning

```bat
python run.py --validate
```

Med Word-fil:

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --extract --validate
```

## Golden Master

Första facitfilen ligger i:

```text
golden_master/parser_facit.yaml
```

Den innehåller verifierade counts för kapitel 6.
