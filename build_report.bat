@echo off
setlocal

echo ==========================================
echo Parser 3.1 Build Report
echo ==========================================

if not exist output mkdir output
if not exist rapportzip mkdir rapportzip
if not exist output\acceptance mkdir output\acceptance
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\trace mkdir output\trace
if not exist output\reports mkdir output\reports
if not exist output\excel mkdir output\excel
if not exist output\word mkdir output\word
if not exist output\archive mkdir output\archive

echo.
echo [1/7] Arbets-Excel profile...
python run.py --profile-master --master "C:\PyProjects\data\Master.xlsx" > output\diagnostics\master_console.txt 2>&1

echo.
echo [2/7] Parser semantic/explain/architecture/missing-debug/trace...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture --missing-debug --trace > output\diagnostics\parser_console.txt 2>&1

echo.
echo [3/7] Parser diff mot Arbets-Excel...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx" >> output\diagnostics\parser_console.txt 2>&1

echo.
echo [4/7] Pytest...
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1

echo.
echo [5/7] Environment info...
python tools\write_environment_report.py > output\diagnostics\environment_report.txt 2>&1

echo.
echo [6/7] Kontroll av rapportfiler...
dir output /s >> output\diagnostics\parser_console.txt 2>&1

echo.
echo [7/7] Skapar zip i rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_output.ps1

echo.
echo ==========================================
echo KLAR
echo Zipfilen finns i rapportzip-mappen.
echo ==========================================

pause
endlocal
