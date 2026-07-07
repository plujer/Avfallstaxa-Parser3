@echo off
setlocal EnableExtensions

 echo ==========================================
 echo Excel Builder - git_commit_block.bat
 echo Block45.2 Commit Status Fix
 echo ==========================================
 echo.

if not exist output\diagnostics\pytest_report.txt (
    echo Ingen pytest_report.txt hittades.
    echo Kor run_project.bat forst.
    pause
    exit /b 1
)

REM Do NOT redirect Python output to latest_run_status.txt.
REM The Python script writes that file itself using safe atomic replacement.
python tools\check_latest_run_status.py
if errorlevel 1 (
    echo.
    echo Senaste testkorningen ar INTE godkand.
    echo Commit stoppad. Kor run_project.bat och atgarda felen.
    pause
    exit /b 1
)

echo.
echo Teststatus godkand. Fortsatter med git commit.
echo.

git status
git add .
git commit -m "Block45.1: Stabilize test automation and commit guard"
if errorlevel 1 (
    echo Commit misslyckades eller inget fanns att committa.
    pause
    exit /b 1
)

git push

echo.
echo BLOCK45.1 COMMIT KLAR
pause
