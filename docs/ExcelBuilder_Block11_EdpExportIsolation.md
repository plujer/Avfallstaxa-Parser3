# Excel Builder Block 11 – EDP Export Isolation

Detta block lägger grunden för den framtida körningen:

```text
Wordfil + en EDP-export → ett unikt Excel-dokument
```

## Viktiga krav

- Varje EDP-export ska skapa ett eget unikt Excel-dokument.
- Malå, Norsjö och Sorsele får inte blandas ihop.
- EDP-data från en kommun får inte användas i en annan kommuns Excel- eller Wordfil.
- Generella regelverk får återanvändas mellan dokument.
- I utvecklingen används Sorsele som primär körning.

## Nya datafiler

```text
data/edp_exports/Mala.xlsx
data/edp_exports/Norsjo.xlsx
data/edp_exports/Sorsele.xlsx
```

## Nya kommandon

Bygg bara Sorsele:

```bat
build_sorsele_excel.bat
```

Bygg alla tre isolerat:

```bat
build_all_edp_exports.bat
```

## Rapportpaket

```bat
build_excel_report.bat
```

Skicka senaste ZIP-filen från:

```text
rapportzip/
```
