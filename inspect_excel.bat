@echo off
setlocal

echo ==========================================
echo Excel Builder - Inspect Arbets-Excel
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

python excel_builder_inspect.py --workbook "C:\PyProjects\data\Master.xlsx" --out "output\excel\arbets_excel_profile_report.txt"

echo.
echo KLAR
echo Rapport finns i output\excel\arbets_excel_profile_report.txt
echo ==========================================

pause
endlocal
