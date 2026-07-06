Write-Host "=========================================="
Write-Host "Parser 3.1 Build Report"
Write-Host "=========================================="

New-Item -ItemType Directory -Force -Path "output" | Out-Null

Write-Host "[1/5] Parser semantic/explain/architecture..."
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture *> output\parser_console.txt

Write-Host "[2/5] Parser diff mot Master.xlsx..."
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx" *>> output\parser_console.txt

Write-Host "[3/5] Pytest..."
python -m pytest -v --tb=short *> output\pytest_report.txt

Write-Host "[4/5] Environment info..."
python tools\write_environment_report.py *> output\environment_report.txt

Write-Host "[5/5] Skapar zip..."
& powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_output.ps1

Write-Host "KLAR - zipfilen finns i output-mappen."
