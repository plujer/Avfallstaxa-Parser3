@echo off
setlocal
if not exist rapportzip mkdir rapportzip
powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1
pause
endlocal
