@echo off
setlocal
set BLOCK_ID=35
set BLOCK_NAME=Hierarchical Context Resolver

echo ==========================================
echo Excel Builder - clean for Block%BLOCK_ID%
echo %BLOCK_NAME%
echo ==========================================
echo.
echo Rensar genererade outputfiler. Data, docs, tester och rapportzip sparas.
echo Tryck Ctrl+C for att avbryta eller valfri tangent for att fortsatta.
pause > nul

if exist output\excel rmdir /s /q output\excel
if exist output\diagnostics rmdir /s /q output\diagnostics
if exist output\reports rmdir /s /q output\reports
if exist output\acceptance rmdir /s /q output\acceptance
if exist output\projects rmdir /s /q output\projects

mkdir output
mkdir output\excel
mkdir output\diagnostics
mkdir output\reports
mkdir output\acceptance
mkdir output\projects

echo.
echo CLEAN KLAR
pause
endlocal
