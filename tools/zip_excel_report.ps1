$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\ExcelBuilder_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null
New-Item -ItemType Directory -Force -Path "output\excel" | Out-Null

$paths = @(
    "output\excel",
    "output\diagnostics\pytest_report.txt",
    "output\reports\parser3_result.json",
    "output\acceptance\parser3_acceptance_report.txt"
)

$existing = @()
foreach ($path in $paths) {
    if (Test-Path $path) {
        $existing += $path
    }
}

if ($existing.Count -eq 0) {
    Write-Host "Inga Excel Builder-rapporter hittades att zippa."
    exit 1
}

Compress-Archive -Path $existing -DestinationPath $zip -Force

$archiveZip = "output\archive\ExcelBuilder_Run_$date.zip"
Copy-Item $zip $archiveZip -Force

Write-Host "ZIP skapad: $zip"
Write-Host "Arkivkopia: $archiveZip"
