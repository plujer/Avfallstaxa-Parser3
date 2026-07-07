# Block50 – Word Excel Mapping 2.0

## Syfte

Inför permanent intern identitet för Word-taxepunkter:

- `WordTaxID` – sectionsbundet ID för exakt spårning i aktuell Word-master.
- `StableTaxIdentity` – sectionsoberoende ID som kan känna igen samma taxepunkt även om den flyttas mellan paragrafer.
- `ContentFingerprint` – hash för maskinell jämförelse mellan versioner.

## Installera

Packa upp ZIP-filen i projektets rotmapp och låt filer skrivas över.

## Kör

```bat
run_project.bat
```

## Skicka tillbaka

Skicka endast senaste ZIP från:

```text
rapportzip\ExcelBuilder_Run_*.zip
```

## Commit

Kör inte `git_commit_block.bat` förrän ChatGPT har granskat rapportzipen och uttryckligen säger att du ska köra commit-scriptet.
