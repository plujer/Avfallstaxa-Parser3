@echo off
setlocal
set BLOCK_ID=36
set BLOCK_NAME=Tax Family Intelligence
set VERSION=v0.9.4

echo ==========================================
echo Excel Builder - tester for Block%BLOCK_ID%
echo %BLOCK_NAME%
echo Version: %VERSION%
echo ==========================================

if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics

python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
set TEST_RESULT=%ERRORLEVEL%

type output\diagnostics\pytest_report.txt

echo.
if %TEST_RESULT% neq 0 (
    echo ==========================================
    echo TESTER MISSLYCKADES
    echo Rapport: output\diagnostics\pytest_report.txt
    echo ==========================================
    pause
    exit /b %TEST_RESULT%
)

echo ==========================================
echo TESTER GODKANDA
    echo Rapport: output\diagnostics\pytest_report.txt
echo ==========================================
pause
endlocal
