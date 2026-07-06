$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zipDir = "rapportzip"
$zip = "$zipDir\Parser3_Run_$date.zip"

New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
New-Item -ItemType Directory -Force -Path "output\archive" | Out-Null

if (-not (Test-Path "output")) {
    Write-Host "Output-mappen saknas."
    exit 1
}

Compress-Archive -Path "output\*" -DestinationPath $zip -Force

$archiveZip = "output\archive\Parser3_Run_$date.zip"
Copy-Item $zip $archiveZip -Force

Write-Host "ZIP skapad: $zip"
Write-Host "Arkivkopia: $archiveZip"
