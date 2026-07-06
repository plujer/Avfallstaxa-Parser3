# Block 13 – Table Engine 2.0

Detta block bevarar tabellceller hela vägen till taxeraden.

Tidigare:

```text
Kärl 240 l (mat-/restavfall) XX kr XX kr XX kr
```

Nu:

```text
name    = Kärl 240 l (mat-/restavfall)
variant = Hämtning varje vecka / var 14:e dag / månadsvis
price   = XX kr
```

## Kör

```bat
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain
```
