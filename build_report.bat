@echo off
setlocal

echo ==========================================
echo Parser 3.1 Build Report
echo ==========================================

if not exist output mkdir output

echo.
echo [1/5] Parser semantic/explain/architecture...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture > output\parser_console.txt 2>&1

echo.
echo [2/5] Parser diff mot Master.xlsx...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx" >> output\parser_console.txt 2>&1

echo.
echo [3/5] Pytest...
python -m pytest -v --tb=short > output\pytest_report.txt 2>&1

echo.
echo [4/5] Environment info...
python tools\write_environment_report.py > output\environment_report.txt 2>&1

echo.
echo [5/5] Skapar zip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_output.ps1

echo.
echo ==========================================
echo KLAR
echo Zipfilen finns i output-mappen.
echo ==========================================

pause
endlocal
