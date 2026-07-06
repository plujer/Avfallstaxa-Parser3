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
echo [1/17] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [2/17] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [3/17] Extraherar taxekunskap...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" > output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [4/17] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [5/17] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [6/17] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [7/17] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [8/17] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [9/17] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [10/17] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [11/17] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [12/17] Kör samlad beslutsmotor...
python excel_builder_decide.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\ArbetsExcel_Reference.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_console.txt 2>&1

echo.
echo [13/17] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [14/17] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1

echo.
echo [15/17] Kör isolerade projekt för alla kommuner...
python excel_builder_project_run.py --config "data\projects\Mala\project_config.json" > output\excel\mala_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Mala\excel\ArbetsExcel_Mala_byggd.xlsx" --municipality "Malå" >> output\excel\mala_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Malå" --edp-export "data\edp_exports\Mala.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Mala\excel\ArbetsExcel_Mala_byggd.xlsx" >> output\excel\mala_project_run_console.txt 2>&1
python excel_builder_project_run.py --config "data\projects\Norsjo\project_config.json" > output\excel\norsjo_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Norsjo\excel\ArbetsExcel_Norsjo_byggd.xlsx" --municipality "Norsjö" >> output\excel\norsjo_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Norsjö" --edp-export "data\edp_exports\Norsjo.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Norsjo\excel\ArbetsExcel_Norsjo_byggd.xlsx" >> output\excel\norsjo_project_run_console.txt 2>&1

echo.
echo [16/17] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo [17/17] Klar.

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
