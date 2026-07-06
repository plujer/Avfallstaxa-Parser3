# Block 10 – Heading Numbering

Word-dokumentet använder automatisk rubriknumrering. `python-docx` läser då rubriktexten utan synligt paragrafnummer.

Exempel i Word:

```text
2.4.6 § Felsorteringsavgift
```

kan i `paragraph.text` bli:

```text
Felsorteringsavgift
```

Block 10 återskapar numreringen från `Heading 1`, `Heading 2`, `Heading 3` osv.

## Testa

```bat
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

Efter detta ska `Context section summary` visa riktiga sektioner, inte vara tom.
