# Block48 – Project Cleanup and Legacy Archive Tool

## Syfte

Block48 inför ett säkert arkivverktyg för äldre projektfiler. Målet är att minska risken
att gamla masterfiler, gamla blockinstallationer och historiska changeloggar används av
misstag i den aktiva pipelinekörningen.

## Viktiga regler

- Aktiva masterfiler ska fortsätta ligga kvar orörda.
- `Taxestruktur_Master_v1.0.docx` får inte ändras.
- `ArbetsExcel_Template_v1.0.xlsx` får inte ändras.
- Äldre filer flyttas till `archive/legacy_project_files/`.
- Källorna i `config/master_sources.json` ändras inte av arkivverktyget.

## Nytt verktyg

```text
archive_legacy_project_files.bat
tools/archive_legacy_project_files.py
```

Verktyget flyttar äldre filer till arkiv och lämnar README-platshållare i historiska
`docs/install` och `docs/changelogg`-mappar så att bakåtkompatibilitet bibehålls.

## Project package

`tools/create_project_package.py` exkluderar nu `archive/` så att arkiverade filer inte
följer med i `project_packages/Project_For_ChatGPT.zip`.
