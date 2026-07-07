@echo off
setlocal
set BLOCK_ID=40
set BLOCK_NAME=Explainable Decision Engine
set VERSION=v0.9.4
set COMMIT_MESSAGE=Block%BLOCK_ID%: %BLOCK_NAME% (%VERSION%)

echo ==========================================
echo Git commit - Block%BLOCK_ID%
echo %BLOCK_NAME%
echo ==========================================

git status

echo.
echo Lagger till andringar...
git add .

echo.
echo Skapar commit:
echo %COMMIT_MESSAGE%
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
    echo.
    echo Commit misslyckades eller inget fanns att committa.
    pause
    exit /b 1
)

echo.
echo Pushar aktuell branch om remote finns...
git push

echo.
echo BLOCK%BLOCK_ID% COMMIT KLAR.
git log -1 --oneline
pause
endlocal
