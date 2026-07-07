@echo off
setlocal
if not exist output\diagnostics mkdir output\diagnostics

echo ==========================================
echo Excel Builder - Block43 tests
 echo ==========================================
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
if errorlevel 1 (
    echo Tester misslyckades. Se output\diagnostics\pytest_report.txt
    type output\diagnostics\pytest_report.txt
    pause
    exit /b 1
)
echo Tester godkända.
type output\diagnostics\pytest_report.txt | findstr /C:"passed"
pause
endlocal
