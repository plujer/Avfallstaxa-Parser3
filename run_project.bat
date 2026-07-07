@echo off
setlocal EnableExtensions

echo ==========================================
echo Excel Builder - run_project.bat
echo Block45 Developer Experience Test Automation
echo ==========================================
echo.
echo Denna fil kor HELA kedjan inklusive pytest i slutet.
echo Du ska normalt bara kora denna fil.
echo.

call build_excel_report.bat
set RESULT=%ERRORLEVEL%

echo.
if "%RESULT%"=="0" (
    echo ==========================================
    echo BLOCK45 VERIFIERING KLAR
    echo ==========================================
    echo Skicka senaste ZIP-filen från rapportzip\
echo Skicka endast senaste ZIP-filen fran rapportzip\
    echo run_tests.bat behovs INTE.
    echo ==========================================
) else (
    echo ==========================================
    echo BLOCK45 MISSLYCKADES
    echo ==========================================
    echo Tester/pipeline har fel.
    echo Skicka senaste ZIP-filen från rapportzip\ om den skapades.
echo Skicka senaste ZIP-filen fran rapportzip\ om den skapades.
    echo Vid behov kan run_tests.bat koras separat, men run_project.bat kor redan tester.
    echo ==========================================
)

pause
exit /b %RESULT%
