@echo off
setlocal
echo Skapar rapportzip...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1
pause
endlocal
