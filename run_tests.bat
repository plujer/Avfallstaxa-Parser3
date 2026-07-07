@echo off
setlocal

echo ==========================================
echo Excel Builder - run_tests.bat
echo ==========================================
echo Denna fil kor ENDAST pytest. Normal korning sker via run_project.bat.
echo.

if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics

python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
set RESULT=%ERRORLEVEL%
python tools\check_latest_run_status.py > output\diagnostics\latest_run_status.txt 2>&1

echo.
type output\diagnostics\latest_run_status.txt
echo.
if "%RESULT%"=="0" (
    echo TESTER OK
) else (
    echo TESTER MISSLYCKADES
)
pause
exit /b %RESULT%
