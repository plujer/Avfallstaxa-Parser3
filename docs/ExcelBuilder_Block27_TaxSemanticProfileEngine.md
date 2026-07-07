# Excel Builder Block 27 – Tax Semantic Profile Engine

Detta block skapar ett gemensamt semantiskt språk för taxor.

## Syfte

Word-taxor, standardtaxor och regler från masterarbetsboken ska översättas till samma profil.

Exempel på profilfält:

- kategori
- avfallstyp
- tjänstetyp
- behållartyp
- behållarvolym
- intervall
- fastighetstyp
- enhetstyp
- faktorhint

## Nya rapporter

```text
output/excel/semantic_profile_report.txt
output/excel/semantic_profiles.csv
```

## Viktigt

Semantiska profiler ändrar inte `Taxa_från_edp`.

De används som nästa underlag för bättre matchning.

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
