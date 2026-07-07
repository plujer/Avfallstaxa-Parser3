@echo off
setlocal
echo Rensar output och temporära rapporter...
if exist output rmdir /s /q output
mkdir output
mkdir output\excel
mkdir output\diagnostics
mkdir output\reports
mkdir output\projects
mkdir output\acceptance
echo Klart.
pause
endlocal
