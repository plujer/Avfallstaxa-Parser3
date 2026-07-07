@echo off
setlocal
set BLOCK_ID=41
set BLOCK_NAME=Workbook Generation Engine
set VERSION=v0.9.4

echo ==========================================
echo Skapar rapportzip - Block%BLOCK_ID%
echo %BLOCK_NAME%
echo ==========================================

powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1
if errorlevel 1 (
    echo Rapportzip misslyckades.
    pause
    exit /b 1
)

echo.
echo Rapportzip skapad. Skicka senaste ZIP-filen fran rapportzip\ till ChatGPT.
pause
endlocal
