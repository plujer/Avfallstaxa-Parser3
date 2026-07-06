$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\Parser3_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null

if (-not (Test-Path "output")) {
    Write-Host "Output-mappen saknas."
    exit 1
}

# Viktigt:
# Zippa inte output\archive, annars packas gamla ZIP-filer in i nya ZIP-filer
# och varje rapportpaket blir större för varje körning.
$paths = @(
    "output\acceptance",
    "output\diagnostics",
    "output\trace",
    "output\reports",
    "output\excel",
    "output\word"
)

$existing = @()
foreach ($path in $paths) {
    if (Test-Path $path) {
        $existing += $path
    }
}

if ($existing.Count -eq 0) {
    Write-Host "Inga output-mappar hittades att zippa."
    exit 1
}

Compress-Archive -Path $existing -DestinationPath $zip -Force

$archiveZip = "output\archive\Parser3_Run_$date.zip"
Copy-Item $zip $archiveZip -Force

Write-Host "ZIP skapad: $zip"
Write-Host "Arkivkopia: $archiveZip"
