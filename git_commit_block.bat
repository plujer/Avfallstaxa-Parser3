@echo off
setlocal
set BLOCK_ID=37
set BLOCK_NAME=Variant Intelligence Engine
set VERSION=v0.9.4
set COMMIT_MESSAGE=Block%BLOCK_ID%: %BLOCK_NAME% (%VERSION%)

echo ==========================================
echo Git commit - Block%BLOCK_ID%
echo %COMMIT_MESSAGE%
echo ==========================================
echo.

git status
if errorlevel 1 (
    echo Git verkar inte vara tillgangligt eller katalogen ar inte ett repo.
    pause
    exit /b 1
)

echo.
echo Skapar commit med alla aktuella andringar.
git add .
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 (
    echo.
    echo Commit skapades inte. Det kan bero pa att det inte finns nagra andringar.
    pause
    exit /b 1
)

echo.
echo Forsoker pusha aktuell branch om remote finns.
git push

echo.
echo ==========================================
echo GIT COMMIT KLAR - Block%BLOCK_ID%
echo ==========================================
git log -1 --oneline
pause
endlocal
