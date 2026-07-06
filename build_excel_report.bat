@echo off
setlocal

echo ==========================================
echo Excel Builder Report Package
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\reports mkdir output\reports
if not exist output\acceptance mkdir output\acceptance
if not exist rapportzip mkdir rapportzip

echo.
echo [1/6] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [2/6] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [3/6] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [4/6] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [5/6] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [6/6] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
