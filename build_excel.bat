@echo off
setlocal

echo ==========================================
echo Excel Builder v2.0.0-alpha.1
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx"

echo.
echo KLAR
echo Resultat finns i output\excel
echo ==========================================

pause
endlocal
