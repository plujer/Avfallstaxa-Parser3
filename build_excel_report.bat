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
echo [1/22] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [2/22] Kontrollerar testsyntax...
python tools\check_test_syntax.py > output\diagnostics\test_syntax_report.txt 2>&1

echo.
echo [3/22] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [4/22] Scannar masterarbetsbokens schema...
python excel_builder_schema_scan.py --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\workbook_schema_console.txt 2>&1

echo.
echo [5/22] Scannar och normaliserar standardtaxekatalog...
python excel_builder_standard_catalog_scan.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_catalog_schema_console.txt 2>&1

echo.
echo [6/22] Extraherar taxekunskap...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" > output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [7/22] Bygger Knowledge Index...
python excel_builder_knowledge_index.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\knowledge_index_console.txt 2>&1

echo.
echo [8/22] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [9/22] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [10/22] Bygger Master Rule Repository...
python excel_builder_rule_repository.py --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\master_rule_repository_console.txt 2>&1

echo.
echo [11/22] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\ArbetsExcel_Reference.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [12/22] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [13/22] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\ArbetsExcel_Reference.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [14/22] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [15/22] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [16/22] Skriver Tax Knowledge till Arbets-Excel...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" >> output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [17/22] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [18/22] Kör samlad beslutsmotor...
python excel_builder_decide.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\ArbetsExcel_Reference.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_console.txt 2>&1

echo.
echo [19/22] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [20/22] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1

echo.
echo [21/22] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo [22/22] Klar.

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
