@echo off
setlocal
echo ==========================================
echo Excel Builder - Tester Block44
echo ==========================================
if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics
python -m pytest -v --tb=short > output\diagnostics\pytest_report.txt 2>&1
type output\diagnostics\pytest_report.txt
if errorlevel 1 (
  echo.
  echo TESTER MISSLYCKADES
  pause
  exit /b 1
)
echo.
echo TESTER KLARA
pause
endlocal
