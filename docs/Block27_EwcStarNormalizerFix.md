# Block 27 – EWC Star Normalizer Fix

Detta block rättar den isolerade normaliseringsbuggen där EWC-kod med stjärna, t.ex. `170601*`, kunde lämna kvar ett `x` efter symbolnormalisering.

## Problem

Tidigare kunde:

```text
Isolering utan innehåll av asbest 170601* kilogram
```

bli:

```text
isolering utan innehåll av asbestxkilogram
```

## Lösning

EWC-regexen använder nu:

```regex
(?<!\d)\d{6}\*?(?!\d)
```

i stället för word-boundary efter `*`.

## Kör

```bat
python -m pytest
build_report.bat
```
