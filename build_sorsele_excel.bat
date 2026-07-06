@echo off
setlocal

echo ==========================================
echo Excel Builder - Sorsele
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

python excel_builder_isolated_run.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --out-dir "output\excel"

echo.
echo KLAR
echo Sorsele-output finns i output\excel\Sorsele
echo ==========================================

pause
endlocal
