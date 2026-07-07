@echo off
setlocal EnableExtensions

 echo ==========================================
 echo Excel Builder - git_commit_block.bat
 echo Block49 Pipeline Controller
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
git commit -m "Block49: Add Pipeline Controller"
if errorlevel 1 (
    echo Commit misslyckades eller inget fanns att committa.
    pause
    exit /b 1
)

git push

echo.
echo BLOCK49 COMMIT KLAR
pause
