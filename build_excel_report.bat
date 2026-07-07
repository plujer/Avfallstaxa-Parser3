@echo off
setlocal EnableExtensions EnableDelayedExpansion

set BLOCK_NAME=Block50 Word Excel Mapping 2.0
set PYTEST_FAILED=0
set PIPELINE_FAILED=0
set WARNING_FAILED=0
set PROJECT_ROOT=%CD%
set PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%

echo ==========================================
echo Excel Builder - %BLOCK_NAME%
echo ==========================================
echo.

if not exist output mkdir output
if not exist output\excel mkdir output\excel
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\reports mkdir output\reports
if not exist output\acceptance mkdir output\acceptance
if not exist output\projects mkdir output\projects
if not exist rapportzip mkdir rapportzip

echo [1/39] Kontrollerar masterkallor...
python tools\check_master_sources.py > output\diagnostics\master_sources_console.txt 2>&1
if errorlevel 1 set WARNING_FAILED=1

echo [2/39] Kontrollerar immutable master enforcement...
python tools\check_immutable_master_enforcement.py > output\diagnostics\immutable_master_enforcement_console.txt 2>&1
if errorlevel 1 set WARNING_FAILED=1

echo [3/39] Kontrollerar v1.0-specifikation...
python tools\check_v1_spec.py > output\diagnostics\v1_spec_report.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [4/39] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [5/39] Kontrollerar testsyntax...
python tools\check_test_syntax.py > output\diagnostics\test_syntax_report.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [6/39] Klassificerar dokumentstruktur...
python excel_builder_document_structure.py --parser-result "output\reports\parser3_result.json" > output\excel\document_structure_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [7/39] Löser parserkontext...
python excel_builder_context_resolve.py --parser-result "output\reports\parser3_result.json" > output\excel\context_resolution_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [8/39] Scannar masterarbetsbokens schema...
python excel_builder_schema_scan.py --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\workbook_schema_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [9/39] Scannar och normaliserar standardtaxekatalog...
python excel_builder_standard_catalog_scan.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_catalog_schema_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [10/39] Tolkar taxekoder...
python excel_builder_tax_codes.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\tax_code_intelligence_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [11/39] Bygger Tax Family Intelligence...
python excel_builder_tax_family.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\tax_family_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [12/39] Bygger Variant Intelligence...
python excel_builder_variant_intelligence.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\variant_intelligence_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [13/39] Bygger Semantic Attribute Intelligence...
python excel_builder_semantic_attributes.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\semantic_attribute_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [14/39] Bygger Composite Matching Engine...
python excel_builder_composite_matching.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\composite_matching_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [15/39] Bygger Explainable Decision Engine...
python excel_builder_decision_explainer.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\explainable_decision_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [16/39] Extraherar taxekunskap...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" > output\excel\tax_knowledge_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [17/39] Bygger Knowledge Index...
python excel_builder_knowledge_index.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\knowledge_index_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [18/39] Bygger semantiska taxaprofiler...
python excel_builder_semantic_profiles.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\semantic_profile_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [19/39] Rankar semantiska kandidater...
python excel_builder_semantic_candidates.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\semantic_candidate_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [20/39] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [21/39] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [22/39] Bygger Master Rule Repository...
python excel_builder_rule_repository.py --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\master_rule_repository_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [23/39] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [24/39] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [25/39] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" > output\excel\excel_matching_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [26/39] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [27/39] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [28/39] Skriver Tax Knowledge till Arbets-Excel...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" >> output\excel\tax_knowledge_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [29/39] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [30/39] Kör gammal beslutsmotor för jämförelse...
python excel_builder_decide.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [31/39] Kör semantisk beslutsmotor...
python excel_builder_decide_semantic.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\master_templates\ArbetsExcel_Template_v1.0.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_semantic_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [32/39] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [33/39] Bygger Word till Excel-mappning...
python excel_builder_word_excel_mapping.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_excel_mapping_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [34/39] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1
python excel_builder_edp_deviations.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [35/39] Kör hela testsviten i slutet av pipeline...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
if errorlevel 1 set PYTEST_FAILED=1

echo [36/39] Sammanfattar senaste teststatus...
python tools\check_latest_run_status.py > output\diagnostics\latest_run_status_console.txt 2>&1
if errorlevel 1 set PYTEST_FAILED=1

echo [37/39] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1
if errorlevel 1 set PIPELINE_FAILED=1

echo [38/39] Skapar aktuellt Project_For_ChatGPT-paket...
python tools\create_project_package.py > output\diagnostics\project_package_console.txt 2>&1
if errorlevel 1 set PIPELINE_FAILED=1

echo [39/39] Skriver samlad pipeline-status...
python tools\pipeline_status.py --block-name "%BLOCK_NAME%" --pipeline-failed %PIPELINE_FAILED% --warnings-failed %WARNING_FAILED% --pytest-failed %PYTEST_FAILED% > output\diagnostics\pipeline_status_console.txt 2>&1
set STATUS_RESULT=%ERRORLEVEL%

echo.
echo ==========================================
echo Excel Builder - KORNING SAMMANFATTNING
echo ==========================================
type output\diagnostics\pipeline_status.txt
echo ==========================================
if "%STATUS_RESULT%"=="0" (
    echo Skicka senaste ZIP-filen från rapportzip\
    echo Skicka senaste ZIP-filen fran rapportzip\
    pause
    exit /b 0
) else (
    echo KORNING MISSLYCKADES. Kor INTE commit-scriptet.
    pause
    exit /b 1
)
