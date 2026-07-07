@echo off
setlocal

echo ==========================================
echo Excel Builder v2.0.0-alpha.2
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

echo.
echo [1/4] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_profile_report.txt"

echo.
echo [2/4] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40

echo.
echo [3/4] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx"

echo.
echo [4/4] Bygger första Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx"

echo.
echo KLAR
echo Resultat finns i output\excel
echo ==========================================

pause
endlocal
