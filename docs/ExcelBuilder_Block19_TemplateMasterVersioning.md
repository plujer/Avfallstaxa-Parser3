# Excel Builder Block 19 – Template Master Versioning

Detta block inför principen att arbetsboken är både:

1. Regelbok
2. Visuell Excel-mall

## Grundregel

Programmet ska inte skapa färdiga arbetsböcker från grunden.

Det ska:

```text
1. kopiera master-/mallarbetsboken
2. bevara utseende, flikar, formler och layout
3. fylla data i kopian
4. aldrig skriva direkt i masterfilen
```

## Master får inte ändras automatiskt

Om det finns behov av:

- nya kolumner,
- nya flikar,
- nya rader,
- ändrade formler,
- ändrad layout,

ska assistenten fråga användaren först.

Efter godkännande skapas en ny versionsbaserad master i:

```text
data/master_templates/
```

Exempel:

```text
ArbetsExcel_Template_v0.2.0_draft.xlsx
ArbetsExcel_Template_v1.0.0_locked.xlsx
```

## Låsning

En fil blir låst master först när användaren uttryckligen säger att den ska låsas.

## Nytt kommando

```bat
build_template_copy.bat
```

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
