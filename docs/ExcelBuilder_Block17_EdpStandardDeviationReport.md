# Excel Builder Block 17 – EDP Standard Deviation Report

Detta block börjar fylla fliken:

```text
EDP_Avviker_Standard
```

## Syfte

Jämföra kommunens befintliga `Taxa_från_edp` mot standardtaxorna.

## Viktigt

Detta block ändrar aldrig `Taxa_från_edp`.

Befintliga kommun-EDP-taxor är fasta. Standardtaxor används endast för:

- avvikelseanalys,
- granskning,
- beslutsstöd.

## Vad skrivs?

Avvikelser skrivs till:

```text
EDP_Avviker_Standard
```

Spårning skrivs till:

```text
Regelspårning
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
