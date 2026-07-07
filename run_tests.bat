@echo off
setlocal
set BLOCK_ID=39
set BLOCK_NAME=Composite Matching Engine
set VERSION=v0.9.4

echo ==========================================
echo Excel Builder testkorning - Block%BLOCK_ID%
echo %BLOCK_NAME%
echo Version: %VERSION%
echo ==========================================

if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics

python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
if errorlevel 1 (
    echo.
    echo TESTER MISSLYCKADES.
    echo Se output\diagnostics\pytest_report.txt
    pause
    exit /b 1
)

echo.
echo ALLA TESTER PASSERADE.
echo Se output\diagnostics\pytest_report.txt
pause
endlocal
