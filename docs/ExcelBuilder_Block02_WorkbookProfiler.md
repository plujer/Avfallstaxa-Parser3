# Excel Builder Block 02 – Workbook Profiler

Detta block analyserar nuvarande Arbets-Excel utan att skriva till den.

## Syfte

Innan vi bygger Matching Engine behöver vi veta hur arbetsboken ser ut:

- blad
- kolumner
- dolda kolumner
- rubrikrad
- Excel-tabeller
- datavalideringar
- formler
- sammanslagna celler

## Nytt kommando

```bat
inspect_excel.bat
```

eller:

```bat
python excel_builder_inspect.py --workbook "C:\PyProjects\data\Master.xlsx"
```

## Rapport

```text
output/excel/arbets_excel_profile_report.txt
```

## Viktigt

Detta är helt läsande analys.

Arbets-Excel ändras inte.
