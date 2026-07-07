@echo off
setlocal

echo ==========================================
echo Excel Builder - Block44 Immutable Master Enforcement
echo ==========================================

echo Kör full verifiering och rapportpaket...
call build_excel_report.bat

if errorlevel 1 (
    echo.
    echo ==========================================
    echo BLOCK44 MISSLYCKADES
    echo ==========================================
    echo Kör vid behov: run_tests.bat
    pause
    exit /b 1
)

echo.
echo ==========================================
echo BLOCK44 VERIFIERING KLAR
echo ==========================================
echo Skicka endast senaste ZIP-filen från rapportzip\
echo run_tests.bat behövs inte om inga fel visas ovan.
echo ==========================================
pause
endlocal
