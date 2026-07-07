@echo off
setlocal

echo ==========================================
echo Rensar temporara output-mappar
echo ==========================================

if exist output\diagnostics del /q output\diagnostics\*.*
if exist output\excel del /q output\excel\*.*
if exist output\reports del /q output\reports\*.*

echo Klar.
pause
endlocal
