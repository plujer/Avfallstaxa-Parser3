@echo off
setlocal

echo ==========================================
echo Excel Builder - run_clean.bat
echo ==========================================

if exist output rmdir /s /q output
if exist rapportzip rmdir /s /q rapportzip
mkdir output
mkdir rapportzip

echo Stadning klar.
pause
