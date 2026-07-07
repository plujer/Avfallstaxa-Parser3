$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\ExcelBuilder_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null
New-Item -ItemType Directory -Force -Path "output\excel" | Out-Null
New-Item -ItemType Directory -Force -Path "output\diagnostics" | Out-Null

$manifest = "output\excel\excel_report_manifest.txt"

$files = @(
    "docs\spec\ExcelBuilder_v1_0_Specification.md",
    "docs\spec\ExcelBuilder_v1_0_Roadmap.md",
    "docs\spec\ExcelBuilder_v1_0_Invariants.md",
    "output\diagnostics\v1_spec_report.txt",
    "output\diagnostics\test_cleanup_report.txt",
    "output\diagnostics\test_syntax_report.txt",
    "output\diagnostics\master_sources_console.txt",
    "output\diagnostics\immutable_master_enforcement_console.txt",
    "output\diagnostics\latest_run_status.txt",
    "output\excel\tax_code_intelligence_report.txt",
    "output\excel\tax_code_intelligence.csv",
    "output\excel\tax_code_intelligence_console.txt",
    "output\excel\tax_family_report.txt",
    "output\excel\tax_families.csv",
    "output\excel\tax_family_console.txt",
    "output\excel\variant_intelligence_report.txt",
    "output\excel\variant_profiles.csv",
    "output\excel\variant_intelligence_console.txt",
    "output\excel\semantic_attribute_report.txt",
    "output\excel\semantic_attributes.csv",
    "output\excel\semantic_attribute_console.txt",
    "output\excel\composite_matching_report.txt",
    "output\excel\composite_matches.csv",
    "output\excel\composite_matching_console.txt",
    "output\excel\explainable_decision_report.txt",
    "output\excel\decision_traces.csv",
    "output\excel\explainable_decision_console.txt",
    "output\excel\context_resolution_report.txt",
    "output\excel\context_resolved_rows.csv",
    "output\excel\document_structure_report.txt",
    "output\excel\document_structure_rows.csv",
    "output\excel\document_structure_console.txt",
    "output\excel\context_resolution_console.txt",
    "output\excel\tax_decision_semantic_report.txt",
    "output\excel\tax_decision_semantic_results.csv",
    "output\excel\tax_decision_semantic_console.txt",
    "output\excel\semantic_candidate_report.txt",
    "output\excel\semantic_candidates.csv",
    "output\excel\semantic_candidate_console.txt",
    "output\excel\semantic_profile_report.txt",
    "output\excel\semantic_profiles.csv",
    "output\excel\semantic_profile_console.txt",
    "output\excel\standard_catalog_schema_report.txt",
    "output\excel\standard_catalog_schema.csv",
    "output\excel\standard_catalog_schema_console.txt",
    "output\excel\EDP_Standardtaxor_normalized.xlsx",
    "output\excel\workbook_schema_report.txt",
    "output\excel\workbook_schema_sheets.csv",
    "output\excel\workbook_schema_header_candidates.csv",
    "output\excel\workbook_schema_console.txt",
    "output\excel\ArbetsExcel_byggd_fran_parser.xlsx",
    "output\excel\master_rule_repository_report.txt",
    "output\excel\master_rule_repository.csv",
    "output\excel\master_rule_repository_console.txt",
    "output\excel\tax_knowledge_report.txt",
    "output\excel\tax_knowledge_features.csv",
    "output\excel\tax_knowledge_console.txt",
    "output\excel\knowledge_index_report.txt",
    "output\excel\knowledge_index.csv",
    "output\excel\knowledge_index_console.txt",
    "output\excel\tax_decision_report.txt",
    "output\excel\tax_decision_results.csv",
    "output\excel\tax_decision_console.txt",
    "output\excel\standard_tax_suggestions_report.txt",
    "output\excel\standard_tax_suggestions.csv",
    "output\excel\standard_tax_suggestions_console.txt",
    "output\projects\Sorsele\excel\ArbetsExcel_Sorsele_byggd.xlsx",
    "output\projects\Sorsele\reports\edp_isolated_run_report_Sorsele.txt",
    "output\projects\Sorsele\manifest\project_run_manifest.json",
    "data\edp_standard\EDP_Future_Standard_Taxor_Renhallning.xlsx",
    "config\master_sources.json",
    "data\master_templates\ArbetsExcel_Template_v1.0.xlsx",
    "data\word_templates\Taxestruktur_Master_v1.0.docx",
    "output\excel\sorsele_project_run_console.txt",
    "output\excel\taxepunkter_row_plan_report.txt",
    "output\excel\taxepunkter_row_plan.csv",
    "output\excel\taxepunkter_row_plan_console.txt",
    "output\excel\word_tax_coverage_report.txt",
    "output\excel\word_tax_coverage_results.csv",
    "output\excel\word_tax_coverage_console.txt",
    "output\excel\excel_matching_results.csv",
    "output\excel\excel_matching_report.txt",
    "output\excel\excel_matching_console.txt",
    "output\excel\arbets_excel_profile_report.txt",
    "output\excel\arbets_excel_snapshot.txt",
    "output\excel\edp_rulebook_report.txt",
    "output\excel\edp_rulebook_console.txt",
    "output\excel\excel_builder_report.txt",
    "output\excel\excel_builder_console.txt",
    "output\excel\excel_inspect_console.txt",
    "output\diagnostics\pytest_report.txt",
    "output\reports\parser3_result.json",
    "output\acceptance\parser3_acceptance_report.txt"
)

$manifestLines = @()
$manifestLines += "Excel Builder Full Report Package"
$manifestLines += "Created: $date"
$manifestLines += ""
$manifestLines += "Included files:"

$existing = @()
foreach ($file in $files) {
    if (Test-Path $file) {
        $existing += $file
        $manifestLines += "[OK] $file"
    } else {
        $manifestLines += "[MISSING] $file"
    }
}

$manifestLines | Out-File -FilePath $manifest -Encoding utf8
$existing += $manifest

if ($existing.Count -eq 0) {
    Write-Host "Inga Excel Builder-rapporter hittades att zippa."
    exit 1
}

Compress-Archive -Path $existing -DestinationPath $zip -Force

$archiveZip = "output\archive\ExcelBuilder_Run_$date.zip"
Copy-Item $zip $archiveZip -Force

Write-Host "ZIP skapad: $zip"
Write-Host "Arkivkopia: $archiveZip"
Write-Host "Manifest: $manifest"
