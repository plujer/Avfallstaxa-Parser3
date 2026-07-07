@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo ==========================================
echo Excel Builder - Block34 verifiering
echo ==========================================
echo.

if not exist output mkdir output
if not exist output\excel mkdir output\excel
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\reports mkdir output\reports
if not exist rapportzip mkdir rapportzip

echo [1/5] Kontrollerar v1.0-specifikation...
python tools\check_v1_spec.py > output\diagnostics\v1_spec_report.txt 2>&1
if errorlevel 1 goto fail_spec

echo [2/5] Kör hela testsviten...
python -m pytest -q > output\diagnostics\pytest_report.txt 2>&1
if errorlevel 1 goto fail_pytest

echo [3/5] Kör Document Structure Engine...
python excel_builder_document_structure.py --parser-result "output\reports\parser3_result.json" > output\excel\document_structure_console.txt 2>&1
if errorlevel 1 goto fail_structure

echo [4/5] Kör semantisk beslutsmotor...
python excel_builder_decide_semantic.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_semantic_console.txt 2>&1
if errorlevel 1 goto fail_semantic

echo [5/5] Skapar rapportzip...
call build_excel_report.bat
if errorlevel 1 goto fail_report

echo.
echo ==========================================
echo BLOCK34 VERIFIERING KLAR
echo ==========================================
echo Skicka tillbaka senaste ZIP-filen fran rapportzip\
echo samt dessa filer om de finns:
echo - output\excel\document_structure_report.txt
echo - output\excel\document_structure_rows.csv
echo - output\diagnostics\pytest_report.txt
echo - output\excel\tax_decision_semantic_results.csv
echo.
pause
exit /b 0

:fail_spec
echo.
echo FEL: v1.0-specifikationen misslyckades.
echo Se output\diagnostics\v1_spec_report.txt
pause
exit /b 1

:fail_pytest
echo.
echo FEL: Tester misslyckades.
echo Se output\diagnostics\pytest_report.txt
pause
exit /b 1

:fail_structure
echo.
echo FEL: Document Structure Engine misslyckades.
echo Se output\excel\document_structure_console.txt
pause
exit /b 1

:fail_semantic
echo.
echo FEL: Semantisk beslutsmotor misslyckades.
echo Se output\excel\tax_decision_semantic_console.txt
pause
exit /b 1

:fail_report
echo.
echo FEL: Rapportzip kunde inte skapas.
echo Se output\diagnostics och output\excel.
pause
exit /b 1
