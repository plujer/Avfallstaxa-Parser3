@echo off
setlocal
set BLOCK_ID=35
set BLOCK_NAME=Hierarchical Context Resolver
set VERSION=v0.9.4

echo ==========================================
echo Excel Builder - Block%BLOCK_ID%
echo %BLOCK_NAME%
echo Version: %VERSION%
echo ==========================================
echo.
echo Detta ar huvudkorningen for aktuellt block.
echo Den kor full pipeline, tester och skapar rapportzip.
echo.

call build_excel_report.bat
if errorlevel 1 (
    echo.
    echo ==========================================
    echo BLOCK%BLOCK_ID% MISSLYCKADES
    echo Kor run_tests.bat om du vill felsoka tester separat.
    echo Skicka annars senaste rapportzip om den skapades.
    echo ==========================================
    pause
    exit /b 1
)

echo.
echo ==========================================
echo BLOCK%BLOCK_ID% KORNING KLAR
echo Skicka endast senaste ZIP-filen fran rapportzip\ till ChatGPT.
echo ==========================================
pause
endlocal
