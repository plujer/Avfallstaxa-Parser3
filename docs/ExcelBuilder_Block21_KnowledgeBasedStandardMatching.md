# Excel Builder Block 21 – Knowledge Based Standard Matching

Detta block kopplar ihop Tax Knowledge Engine med standardtaxeförslag.

## Vad som ändras

Tidigare jämfördes mest taxanamnet mot standardtaxans benämning.

Nu vägs flera saker in:

- namnlikhet
- nyckelord
- avfallstyp
- faktorhint
- kategori
- enhetstyp

## Viktigt

Standardtaxor är fortfarande endast förslag.

De får aldrig skriva över befintlig kommun-EDP i `Taxa_från_edp`.

## Förväntad effekt

Fler rader bör kunna få:

```text
STANDARD_PROPOSAL
```

eller:

```text
REVIEW_REQUIRED
```

i stället för att bli `NEW_TAXA`.

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
