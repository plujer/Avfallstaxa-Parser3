@echo off
setlocal
echo Rensar output och temporära verifieringsfiler...
if exist output rmdir /s /q output
if not exist output mkdir output
if not exist output\diagnostics mkdir output\diagnostics
if not exist output\excel mkdir output\excel
echo Klar.
pause
endlocal
