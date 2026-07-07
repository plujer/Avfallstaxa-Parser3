@echo off
setlocal

echo ==========================================
echo Excel Builder Report Package
echo ==========================================

if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\excel mkdir output\excel
if not exist rapportzip mkdir rapportzip

echo.
echo [1/4] Kontrollerar v1.0-specifikation...
python tools\check_v1_spec.py > output\diagnostics\v1_spec_report.txt 2>&1

echo.
echo [2/4] Kontrollerar testsyntax...
python tools\check_test_syntax.py > output\diagnostics\test_syntax_report.txt 2>&1

echo.
echo [3/4] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [4/4] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
