@echo off
setlocal
set BLOCK_ID=38
set BLOCK_NAME=Semantic Attribute Intelligence
set VERSION=v0.9.4
set TAG=%VERSION%-block%BLOCK_ID%

echo ==========================================
echo Git release - Block%BLOCK_ID%
echo Tagg: %TAG%
echo ==========================================
echo.

git diff --quiet
if errorlevel 1 (
    echo Arbetskatalogen har okommittade andringar. Kor git_commit_block.bat forst.
    pause
    exit /b 1
)

git tag -a %TAG% -m "Verified Block%BLOCK_ID%: %BLOCK_NAME%"
if errorlevel 1 (
    echo Taggen kunde inte skapas. Finns den redan?
    pause
    exit /b 1
)

git push
git push origin %TAG%

echo.
echo ==========================================
echo BLOCK%BLOCK_ID% RELEASE KLAR
echo Tag: %TAG%
echo ==========================================
pause
endlocal
