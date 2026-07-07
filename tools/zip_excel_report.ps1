$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\ExcelBuilder_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null
New-Item -ItemType Directory -Force -Path "output\excel" | Out-Null
New-Item -ItemType Directory -Force -Path "output\diagnostics" | Out-Null

$manifest = "output\excel\excel_report_manifest.txt"

$files = @(
    "output\diagnostics\test_cleanup_report.txt",
    "output\diagnostics\test_syntax_report.txt",
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
    "output\excel\sorsele_project_run_console.txt",
    "output\diagnostics\pytest_report.txt",
    "output\reports\parser3_result.json",
    "output\acceptance\parser3_acceptance_report.txt"
)

$manifestLines = @()
$manifestLines += "Excel Builder Report Package"
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
