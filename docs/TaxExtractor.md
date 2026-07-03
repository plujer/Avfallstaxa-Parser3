# Tax Extractor

Block 4 lägger till preliminär extraktion av `TaxRow`.

## Körning

```bat
python run.py --word "C:\sokvag\Taxestruktur.docx" --extract
```

Skapar:

```text
output/parser3_result.json
output/parser3_report.txt
```

## Viktigt

Detta är ännu inte slutlig parserlogik. Det är första extraktionsmotorn som senare ska kopplas till golden master.
