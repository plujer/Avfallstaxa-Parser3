@echo off
setlocal

echo ==========================================
echo Excel Builder v2.0.0-alpha.1
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

echo.
echo [1/3] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "C:\PyProjects\data\Master.xlsx" --out "output\excel\arbets_excel_profile_report.txt"

echo.
echo [2/3] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "C:\PyProjects\data\Master.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40

echo.
echo [3/3] Bygger första Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx"

echo.
echo KLAR
echo Resultat finns i output\excel
echo ==========================================

pause
endlocal
