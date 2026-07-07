$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\ExcelBuilder_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null
New-Item -ItemType Directory -Force -Path "output\diagnostics" | Out-Null

$manifest = "output\excel\excel_report_manifest.txt"
New-Item -ItemType Directory -Force -Path "output\excel" | Out-Null

$files = @(
    "docs\spec\ExcelBuilder_v1_0_Specification.md",
    "docs\spec\ExcelBuilder_v1_0_Roadmap.md",
    "docs\spec\ExcelBuilder_v1_0_Invariants.md",
    "output\diagnostics\v1_spec_report.txt",
    "output\diagnostics\test_syntax_report.txt",
    "output\diagnostics\pytest_report.txt"
)

$manifestLines = @()
$manifestLines += "Excel Builder v1.0 Specification Report Package"
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

Compress-Archive -Path $existing -DestinationPath $zip -Force

$archiveZip = "output\archive\ExcelBuilder_Run_$date.zip"
Copy-Item $zip $archiveZip -Force

Write-Host "ZIP skapad: $zip"
Write-Host "Arkivkopia: $archiveZip"
Write-Host "Manifest: $manifest"
