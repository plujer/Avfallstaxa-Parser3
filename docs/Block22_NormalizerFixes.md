# Block 22 – Normalizer Fixes

Detta block förbättrar normaliseringen och §6.1.2-matchningen.

## Fixar

- `×`, `*` och `x` behandlas som samma separator.
- EWC-koder och UN-nummer tas bort vid acceptance-jämförelse.
- Slutliga enheter som `kilogram`, `m³`, `styck` tas bort vid namnmatchning.
- `Section612Extractor` använder kontrollerad fuzzy matchning för mindre Word-skillnader.

## Mål

Att få de fyra kvarvarande §6.1.2-raderna att matcha:

- Skrymmande avfall till energiåtervinning större än 20×20×80
- Isolering utan innehåll av asbest
- WC-stol
- Stubbar/rötter för krossning

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --missing-debug
python -m pytest
build_report.bat
```
