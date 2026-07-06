# Excel Builder Block 18 – Decision Engine Status

Detta block inför en samlad beslutsmotor.

## Syfte

För varje Word/parser-taxa ska systemet sätta en tydlig status:

```text
EDP_MATCH
STANDARD_PROPOSAL
REVIEW_REQUIRED
NEW_TAXA
```

## Prioritet

```text
1. Bekräftad kommun-EDP / Taxa_från_edp
2. Word-taxa
3. Standardtaxor endast som förslag
4. Manuell granskning
```

## Nya resultat

I `Taxepunkter` läggs kolumner till:

```text
Beslutsstatus
Beslutsregel
Beslutskommentar
```

I `Regelspårning` skrivs beslutsrader.

## Viktigt

Befintlig `Taxa_från_edp` ändras inte.

## Kör tester

```bat
python -m pytest
```

## Bygg rapportpaket

```bat
build_excel_report.bat
```

## Skicka tillbaka

```text
rapportzip/
```
