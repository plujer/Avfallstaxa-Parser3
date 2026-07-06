# Block 29 – Output Structure + Unit Split

Detta block inför den output-struktur vi bestämde:

```text
output/
├── acceptance/
├── diagnostics/
├── trace/
├── reports/
├── excel/
├── word/
└── archive/
```

## Viktigt

ZIP-filen för återrapportering skapas nu i:

```text
docs/
```

Output för framtida Word-generator finns nu här:

```text
output/word/
```

## Dessutom

`FlatTaxExtractor` separerar nu enhet från namn när priset står som t.ex.:

```text
XXXX kr/fraktion
XX kr/besök
```

så att `/fraktion` och `/besök` inte hamnar i taxapunktens namn.

## Kör

```bat
python -m pytest
build_report.bat
```
