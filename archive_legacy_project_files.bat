@echo off
setlocal

echo.
echo Excel Builder - archive legacy project files
echo.

python tools\archive_legacy_project_files.py
set ERR=%ERRORLEVEL%

echo.
if "%ERR%"=="0" (
    echo Archive step complete.
) else (
    echo Archive step failed. Errorlevel: %ERR%
)

pause
exit /b %ERR%
