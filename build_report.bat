@echo off
setlocal

echo ==========================================
echo Parser 3.1 Build Report
echo ==========================================

if not exist output mkdir output

echo.
echo [1/7] Arbets-Excel profile...
python run.py --profile-master --master "C:\PyProjects\data\Master.xlsx" > output\master_console.txt 2>&1

echo.
echo [2/7] Parser semantic/explain/architecture/missing-debug/trace...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --explain --architecture --missing-debug --trace > output\parser_console.txt 2>&1

echo.
echo [3/7] Parser diff mot Arbets-Excel...
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --diff --master "C:\PyProjects\data\Master.xlsx" >> output\parser_console.txt 2>&1

echo.
echo [4/7] Pytest...
python -m pytest -v --tb=short > output\pytest_report.txt 2>&1

echo.
echo [5/7] Environment info...
python tools\write_environment_report.py > output\environment_report.txt 2>&1

echo.
echo [6/7] Kontroll av rapportfiler...
dir output >> output\parser_console.txt 2>&1

echo.
echo [7/7] Skapar zip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_output.ps1

echo.
echo ==========================================
echo KLAR
echo Zipfilen finns i output-mappen.
echo ==========================================

pause
endlocal
