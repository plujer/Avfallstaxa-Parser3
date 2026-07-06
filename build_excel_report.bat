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
echo [1/11] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [2/11] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [3/11] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [4/11] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [5/11] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [6/11] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [7/11] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [8/11] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [9/11] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [10/11] Kör isolerad Sorsele EDP-körning...
python excel_builder_isolated_run.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --out-dir "output\excel" > output\excel\sorsele_isolated_run_console.txt 2>&1

echo.
echo [11/11] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
