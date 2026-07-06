# Install Excel Builder Block 01

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python -m pytest
build_report.bat
build_excel.bat
```

Resultat:

```text
output/excel/ArbetsExcel_byggd_fran_parser.xlsx
output/excel/excel_builder_report.txt
```

Commit:

```bat
git add .
git commit -m "Excel Builder Block01 Bootstrap"
git push
```
