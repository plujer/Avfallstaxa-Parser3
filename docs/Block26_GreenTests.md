# Block 26 – Green Tests

Detta block åtgärdar två regressionsfel efter §6.1.2-fixen.

## Fixar

1. `NameNormalizer` tar nu bort EWC-koder med stjärna innan `*` normaliseras till `x`.
2. `test_tax_pipeline_runs_single_official_flow` har justerats till aktuell parserregel:
   kapitel 1 exporteras inte som taxor.

## Varför

§6.1.2 är nu verifierad 103/103. Innan vi går vidare med §6.1.1, §6.1.3 och §6.1.4 ska testsviten bli grön igen.

## Kör

```bat
python -m pytest
build_report.bat
```
