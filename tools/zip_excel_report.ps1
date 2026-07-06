$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\ExcelBuilder_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null
New-Item -ItemType Directory -Force -Path "output\excel" | Out-Null
New-Item -ItemType Directory -Force -Path "output\diagnostics" | Out-Null

$manifest = "output\excel\excel_report_manifest.txt"

$files = @(
    "output\excel\ArbetsExcel_byggd_fran_parser.xlsx",
    "output\excel\excel_matching_results.csv",
    "output\excel\excel_matching_report.txt",
    "output\excel\excel_matching_console.txt",
    "output\excel\arbets_excel_profile_report.txt",
    "output\excel\arbets_excel_snapshot.txt",
    "output\excel\excel_builder_report.txt",
    "output\excel\excel_builder_console.txt",
    "output\excel\excel_inspect_console.txt",
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
