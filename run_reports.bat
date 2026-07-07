@echo off
setlocal
set BLOCK_ID=37
set BLOCK_NAME=Variant Intelligence Engine
set VERSION=v0.9.4

echo ==========================================
echo Excel Builder - rapportzip for Block%BLOCK_ID%
echo %BLOCK_NAME%
echo Version: %VERSION%
echo ==========================================

powershell -NoProfile -ExecutionPolicy Bypass -File tools\zip_excel_report.ps1
if errorlevel 1 (
    echo Rapportzip misslyckades.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo RAPPORTZIP KLAR
echo Skicka senaste ZIP-filen fran rapportzip\ till ChatGPT.
echo ==========================================
pause
endlocal
