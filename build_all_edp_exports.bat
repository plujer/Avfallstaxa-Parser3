@echo off
setlocal

echo ==========================================
echo Excel Builder - Alla EDP-exporter
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel

python excel_builder_isolated_run.py --municipality "Malå" --edp-export "data\edp_exports\Mala.xlsx" --out-dir "output\excel"
python excel_builder_isolated_run.py --municipality "Norsjö" --edp-export "data\edp_exports\Norsjo.xlsx" --out-dir "output\excel"
python excel_builder_isolated_run.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --out-dir "output\excel"

echo.
echo KLAR
echo Separata dokument finns i output\excel\Mala, output\excel\Norsjo och output\excel\Sorsele
echo ==========================================

pause
endlocal
