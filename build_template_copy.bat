@echo off
setlocal

echo ==========================================
echo Excel Builder - Template Copy
echo ==========================================

if not exist output mkdir output
if not exist output\template_test mkdir output\template_test

python excel_builder_template_copy.py --out "output\template_test\ArbetsExcel_TemplateCopy_Test.xlsx"

echo.
echo KLAR
echo Kopia finns i output\template_test
echo ==========================================

pause
endlocal
