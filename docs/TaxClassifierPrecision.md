# Block 12 – Tax Classifier Precision

Detta block stoppar parsern från att exportera normal löptext som taxa.

## Viktiga ändringar

Taxarad kräver nu explicit pris, t.ex.

- `XX kr`
- `XXX kr`
- `22,88`
- `22,88 kr`

Orden `avgift`, `tömning`, `kärl`, `fraktion` räcker inte längre ensamma.

Kapitel 1 exporteras aldrig som taxor.

## Körning

```bat
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain
```
