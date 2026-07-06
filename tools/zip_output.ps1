$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$zip = "output\Parser3_Run_$date.zip"

$files = @(
    "output\parser3_result.json",
    "output\parser3_report.txt",
    "output\parser3_precision_report.txt",
    "output\parser3_explain_report.txt",
    "output\parser3_architecture_report.txt",
    "output\pytest_report.txt",
    "output\parser_console.txt",
    "output\master_console.txt",
    "output\master_profile_report.txt",
    "output\environment_report.txt"
)

$existing = @()
foreach ($file in $files) {
    if (Test-Path $file) {
        $existing += $file
    }
}

if ($existing.Count -eq 0) {
    Write-Host "Inga rapportfiler hittades i output."
    exit 1
}

Compress-Archive -Path $existing -DestinationPath $zip -Force
Write-Host "ZIP skapad: $zip"
