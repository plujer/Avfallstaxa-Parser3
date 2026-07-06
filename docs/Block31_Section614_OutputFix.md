# Block 31 – §6.1.4 + Output Fix

Detta block gör två saker:

1. Slutför §6.1.4 genom att hantera den delade raden:
   `Ombud för registrering av El-kretsen avlämnarintyg i Hämtplatsportalen`.
2. Tar bort flyttsteget som orsakade `PermissionError` i Windows.

## Output

Rapporter skrivs nu direkt till rätt undermappar:

```text
output/
├── acceptance/
├── diagnostics/
├── trace/
├── reports/
├── excel/
├── word/
└── archive/
```

ZIP-filen skapas i:

```text
rapportzip/
```

## Kör

```bat
python -m pytest
build_report.bat
```
