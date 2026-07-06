# Block 9 – Context Engine

Context Engine håller aktuell paragraf aktiv över efterföljande text och tabeller.

## Körning

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
```

Semantisk parser:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```

## Målet med blocket

Taxarader ska inte längre hamna under tom sektion eller felaktig sektion.
