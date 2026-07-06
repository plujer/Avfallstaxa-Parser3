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
if not exist output\projects mkdir output\projects
if not exist rapportzip mkdir rapportzip

echo.
echo [1/14] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [2/14] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [3/14] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [4/14] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [5/14] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [6/14] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [7/14] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [8/14] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [9/14] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [10/14] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [11/14] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [12/14] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1

echo.
echo [13/14] Kör isolerade projekt för alla kommuner...
python excel_builder_project_run.py --config "data\projects\Mala\project_config.json" > output\excel\mala_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Mala\excel\ArbetsExcel_Mala_byggd.xlsx" --municipality "Malå" >> output\excel\mala_project_run_console.txt 2>&1
python excel_builder_project_run.py --config "data\projects\Norsjo\project_config.json" > output\excel\norsjo_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Norsjo\excel\ArbetsExcel_Norsjo_byggd.xlsx" --municipality "Norsjö" >> output\excel\norsjo_project_run_console.txt 2>&1

echo.
echo [14/14] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
