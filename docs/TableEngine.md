# Table Engine

Block 3 lägger till första tabellmotorn.

## Innehåll

- Native Word table reader
- Visual table detector
- Cell normalizer
- Table continuation detector
- Table splitter
- Row classifier
- Reference detector
- Info detector
- Tax row detector

## Körning

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --tables
```

## Viktig parserregel

Varje rad klassificeras innan export:

- tax
- header
- reference
- info
- empty
