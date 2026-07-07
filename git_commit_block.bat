@echo off
setlocal EnableExtensions

 echo ==========================================
 echo Excel Builder - git_commit_block.bat
 echo Block50 Word Excel Mapping 2.0
 echo ==========================================
 echo.

if not exist output\diagnostics\pipeline_status.json (
    echo pipeline_status.json saknas.
    echo Kor run_project.bat forst.
    pause
    exit /b 1
)

python tools\check_pipeline_commit_ready.py
if errorlevel 1 (
    echo.
    echo Senaste pipeline ar INTE godkand for commit.
    echo Commit stoppad. Kor run_project.bat och skicka rapportzip for granskning.
    pause
    exit /b 1
)

echo.
echo Teststatus godkand. Fortsatter med git commit.
echo.

git status
git add .
git commit -m "Block50: Add stable Word Excel Mapping identities"
if errorlevel 1 (
    echo Commit misslyckades eller inget fanns att committa.
    pause
    exit /b 1
)

git push

echo.
echo BLOCK50 COMMIT KLAR
pause
