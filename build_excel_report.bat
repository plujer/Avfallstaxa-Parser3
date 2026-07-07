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
echo [1/30] Kontrollerar v1.0-specifikation...
python tools\check_v1_spec.py > output\diagnostics\v1_spec_report.txt 2>&1

echo.
echo [2/30] Rensar dubbletter i teststruktur...
python tools\cleanup_duplicate_tests.py > output\diagnostics\test_cleanup_report.txt 2>&1

echo.
echo [3/30] Kontrollerar testsyntax...
python tools\check_test_syntax.py > output\diagnostics\test_syntax_report.txt 2>&1

echo.
echo [4/30] Kör tester...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [5/30] Klassificerar dokumentstruktur...
python excel_builder_document_structure.py --parser-result "output\reports\parser3_result.json" > output\excel\document_structure_console.txt 2>&1

echo.
echo [6/30] Löser parserkontext...
python excel_builder_context_resolve.py --parser-result "output\reports\parser3_result.json" > output\excel\context_resolution_console.txt 2>&1

echo.
echo [7/30] Scannar masterarbetsbokens schema...
python excel_builder_schema_scan.py --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\workbook_schema_console.txt 2>&1

echo.
echo [8/30] Scannar och normaliserar standardtaxekatalog...
python excel_builder_standard_catalog_scan.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_catalog_schema_console.txt 2>&1

echo.
echo [9/30] Tolkar taxekoder...
python excel_builder_tax_codes.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\tax_code_intelligence_console.txt 2>&1

echo.
echo [10/34] Bygger Tax Family Intelligence...
python excel_builder_tax_family.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\tax_family_console.txt 2>&1

echo.
echo [11/34] Bygger Variant Intelligence...
python excel_builder_variant_intelligence.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\variant_intelligence_console.txt 2>&1

echo.
echo [12/34] Bygger Semantic Attribute Intelligence...
python excel_builder_semantic_attributes.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\semantic_attribute_console.txt 2>&1

echo.
echo [13/34] Bygger Composite Matching Engine...
python excel_builder_composite_matching.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\composite_matching_console.txt 2>&1



echo.
echo [14/34] Bygger Explainable Decision Engine...
python excel_builder_decision_explainer.py --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\explainable_decision_console.txt 2>&1


echo.
echo [15/34] Extraherar taxekunskap...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" > output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [16/34] Bygger Knowledge Index...
python excel_builder_knowledge_index.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\knowledge_index_console.txt 2>&1

echo.
echo [17/34] Bygger semantiska taxaprofiler...
python excel_builder_semantic_profiles.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\semantic_profile_console.txt 2>&1

echo.
echo [18/34] Rankar semantiska kandidater...
python excel_builder_semantic_candidates.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\semantic_candidate_console.txt 2>&1

echo.
echo [19/34] Profilerar Arbets-Excel...
python excel_builder_inspect.py --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --out "output\excel\arbets_excel_profile_report.txt" > output\excel\excel_inspect_console.txt 2>&1

echo.
echo [20/34] Läser EDP-regelverk...
python excel_builder_rulebook.py --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --out "output\excel\edp_rulebook_report.txt" > output\excel\edp_rulebook_console.txt 2>&1

echo.
echo [21/34] Bygger Master Rule Repository...
python excel_builder_rule_repository.py --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\master_rule_repository_console.txt 2>&1

echo.
echo [22/34] Skapar Arbets-Excel snapshot...
python excel_builder_snapshot.py --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --out "output\excel\arbets_excel_snapshot.txt" --max-rows 40 >> output\excel\excel_inspect_console.txt 2>&1

echo.
echo [23/34] Bygger Taxepunkter row plan...
python excel_builder_row_plan.py --parser-result "output\reports\parser3_result.json" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\taxepunkter_row_plan_console.txt 2>&1

echo.
echo [24/34] Kör Matching Engine preview...
python excel_builder_match.py --parser-result "output\reports\parser3_result.json" --workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" > output\excel\excel_matching_console.txt 2>&1

echo.
echo [25/34] Skapar standardtaxeförslag...
python excel_builder_standard_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" > output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [26/34] Bygger Arbets-Excel från parseroutput...
python excel_builder_cli.py --parser-result "output\reports\parser3_result.json" --out "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\excel_builder_console.txt 2>&1

echo.
echo [27/34] Skriver Tax Knowledge till Arbets-Excel...
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" >> output\excel\tax_knowledge_console.txt 2>&1

echo.
echo [28/34] Skriver standardtaxeförslag till Arbets-Excel...
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" --municipality "" >> output\excel\standard_tax_suggestions_console.txt 2>&1

echo.
echo [29/34] Kör gammal beslutsmotor för jämförelse...
python excel_builder_decide.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_console.txt 2>&1

echo.
echo [30/34] Kör semantisk beslutsmotor...
python excel_builder_decide_semantic.py --parser-result "output\reports\parser3_result.json" --reference-workbook "data\master_templates\ArbetsExcel_Template_v0.9.4_draft.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\tax_decision_semantic_console.txt 2>&1

echo.
echo [31/34] Validerar att alla Word-taxor finns i Taxepunkter...
python excel_builder_coverage.py --parser-result "output\reports\parser3_result.json" --workbook "output\excel\ArbetsExcel_byggd_fran_parser.xlsx" > output\excel\word_tax_coverage_console.txt 2>&1

echo.
echo [32/34] Kör isolerad Sorsele projektkörning...
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json" > output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_tax_knowledge.py --parser-result "output\reports\parser3_result.json" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_apply_suggestions.py --parser-result "output\reports\parser3_result.json" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" --municipality "Sorsele" >> output\excel\sorsele_project_run_console.txt 2>&1
python excel_builder_edp_deviations.py --municipality "Sorsele" --edp-export "data\edp_exports\Sorsele.xlsx" --standard-tax "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx" --workbook "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx" >> output\excel\sorsele_project_run_console.txt 2>&1

echo.
echo [33/34] Skapar standardiserad rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1

echo.
echo [34/34] Klar.

echo.
echo ==========================================
echo KLAR
echo Skicka senaste ZIP-filen från rapportzip till ChatGPT.
echo ==========================================

pause
endlocal
