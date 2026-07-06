# Block 16 – Facit/Master Reader

Detta block gör att vi kan verifiera parsern mot riktig `Master.xlsx`.

## Nytt

- WorkbookProfiler analyserar alla blad.
- MasterExcelReader väljer bästa bladet automatiskt.
- Rapport skapas: `output/master_profile_report.txt`.
- `build_report.bat` inkluderar Master-profilering.

## Kör endast masterprofil

```bat
python run.py --profile-master --master "C:\PyProjects\data\Master.xlsx"
```

## Kör hela rapportpaketet

```bat
build_report.bat
```

Skicka sedan ZIP-filen från output-mappen.
