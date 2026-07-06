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
echo [1/8] Arbets-Excel profile...
python run.py --profile-master --master "C:\PyProjects\data\Master.xlsx" > output\master_console.txt 2>&1

echo.
echo [2/8] Parser semantic/explain/architecture/missing-debug/trace...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture --missing-debug --trace > output\parser_console.txt 2>&1

echo.
echo [3/8] Parser diff mot Arbets-Excel...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx" >> output\parser_console.txt 2>&1

echo.
echo [4/8] Pytest...
python -m pytest -v --tb=short > output\pytest_report.txt 2>&1

echo.
echo [5/8] Environment info...
python tools\write_environment_report.py > output\environment_report.txt 2>&1

echo.
echo [6/8] Organiserar output...
python tools\organize_output.py >> output\parser_console.txt 2>&1

echo.
echo [7/8] Kontroll av rapportfiler...
dir output /s >> output\diagnostics\parser_console.txt 2>&1

echo.
echo [8/8] Skapar zip i rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_output.ps1

echo.
echo ==========================================
echo KLAR
echo Zipfilen finns i rapportzip-mappen.
echo ==========================================

pause
endlocal
