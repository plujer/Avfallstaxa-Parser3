@echo off
setlocal

echo ==========================================
echo Excel Builder Full Report Package
echo ==========================================

if not exist output mkdir output
if not exist output\excel mkdir output\excel
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\reports mkdir output\reports
if not exist output\acceptance mkdir output\acceptance
if not exist output\projects mkdir output\projects
if not exist rapportzip mkdir rapportzip

echo.
echo [1/29] Kontrollerar masterkällor...
python tools\check_master_sources.py > output\diagnostics\master_sources_console.txt 2>&1

echo.
echo [2/29] Kontrollerar v1.0-specifikation...
python tools\check_v1_spec.py > output\diagnostics\v1_spec_report.txt 2>&1

echo.
echo [3/29] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [4/29] Kontrollerar testsyntax...
python tools\check_test_syntax.py > output\diagnostics\test_syntax_report.txt 2>&1

echo.
echo [5/29] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [6/29] Löser parserkontext...
python excel_builder_context_resolve.py --parser-result "output\reports\parser3_result.json" > output\excel\context_resolution_console.txt 2>&1

echo.
echo [7/29] Scannar masterarbetsbokens schema...
python excel_builder_schema_scan.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\workbook_schema_console.txt 2>&1

echo.
echo [8/29] Scannar och normaliserar standardtaxekatalog...
python excel_builder_standard_catalog_scan.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_catalog_schema_console.txt 2>&1

echo.
echo [9/29] Tolkar taxekoder...
python excel_builder_tax_codes.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\tax_code_intelligence_console.txt 2>&1

echo.
echo [10/29] Extraherar taxekunskap...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" > output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [11/29] Bygger Knowledge Index...
python excel_builder_knowledge_index.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\knowledge_index_console.txt 2>&1

echo.
echo [12/29] Bygger semantiska taxaprofiler...
python excel_builder_semantic_profiles.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\semantic_profile_console.txt 2>&1

echo.
echo [13/29] Rankar semantiska kandidater...
python excel_builder_semantic_candidates.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\semantic_candidate_console.txt 2>&1

echo.
echo [14/29] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [15/29] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [16/29] Bygger Master Rule Repository...
python excel_builder_rule_repository.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\master_rule_repository_console.txt 2>&1

echo.
echo [17/29] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [18/29] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [19/29] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [20/29] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [21/29] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [22/29] Skriver Tax Knowledge till Arbets-Excel...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" >> output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [23/29] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [24/29] Kör gammal beslutsmotor för jämförelse...
python excel_builder_decide.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_console.txt 2>&1

echo.
echo [25/29] Kör semantisk beslutsmotor...
python excel_builder_decide_semantic.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data/master_templates/ArbetsExcel_Template_v1.0.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_semantic_console.txt 2>&1

echo.
echo [26/29] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [27/29] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1

echo.
echo [28/29] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo [29/29] Klar.

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
