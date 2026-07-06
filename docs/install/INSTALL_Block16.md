# Install Block16 Facit/Master Reader

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Verifiera:

```bat
python run.py --profile-master --master "C:\PyProjects\data\Master.xlsx"
python -m pytest
build_report.bat
```

Commit:

```bat
git add .
git commit -m "Parser3 Block16 Facit Master Reader"
git push
```
