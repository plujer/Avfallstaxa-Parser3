# Install Excel Builder Block 05

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kontrollera att referensarbetsboken finns här:

```text
data/ArbetsExcel_Reference.xlsx
```

Kör:

```bat
python -m pytest
build_excel_report.bat
```

Skicka senaste ZIP-filen från:

```text
rapportzip/
```

Commit:

```bat
git add .
git commit -m "Excel Builder Block05 Matching Engine Bootstrap"
git push
```
