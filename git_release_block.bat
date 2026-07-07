@echo off
setlocal
set BLOCK_ID=39
set BLOCK_NAME=Composite Matching Engine
set VERSION=v0.9.4
set TAG=%VERSION%-block%BLOCK_ID%

echo ==========================================
echo Git release - Block%BLOCK_ID%
echo %BLOCK_NAME%
echo ==========================================

git status --porcelain > .git_status_check.tmp
for %%A in (.git_status_check.tmp) do set SIZE=%%~zA
if not "%SIZE%"=="0" (
    del .git_status_check.tmp
    echo Arbetskatalogen ar inte ren. Kor git_commit_block.bat forst.
    pause
    exit /b 1
)
del .git_status_check.tmp

echo Skapar tagg %TAG%
git tag -a %TAG% -m "Verified Block%BLOCK_ID% - %BLOCK_NAME%"
if errorlevel 1 (
    echo Taggning misslyckades.
    pause
    exit /b 1
)

git push
git push origin %TAG%

echo.
echo BLOCK%BLOCK_ID% RELEASE KLAR
echo Tag: %TAG%
pause
endlocal
