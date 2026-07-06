# Block 30 – §6.1.3 + rapportzip

Detta block gör två saker:

1. Flyttar återrapporterings-ZIP till projektrotens `rapportzip/`.
2. Lägger in radnivåfacit för §6.1.3 och tillåter tre identiska `Container X m³`-rader.

## Ny rapportstruktur

```text
rapportzip/
└── Parser3_Run_YYYY-MM-DD_HH-mm-ss.zip
```

`output/archive/` får fortfarande en arkivkopia.

## Facit §6.1.3

- Container X m³
- Container X m³
- Container X m³
- Omklassning av felsorterad container

## Kör

```bat
python -m pytest
build_report.bat
```
