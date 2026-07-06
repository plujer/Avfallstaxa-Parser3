@echo off
setlocal

echo ==========================================
echo Excel Builder - Inspect Arbets-Excel
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

python excel_builder_inspect.py --workbook "C:\PyProjects\data\Master.xlsx" --out "output\excel\arbets_excel_profile_report.txt"
python excel_builder_snapshot.py --workbook "C:\PyProjects\data\Master.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40

echo.
echo KLAR
echo Rapporter finns i output\excel
echo ==========================================

pause
endlocal
