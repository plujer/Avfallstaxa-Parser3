@echo off
setlocal

echo.
echo Excel Builder - create project package
echo.

python tools\create_project_package.py
set ERR=%ERRORLEVEL%

echo.
if "%ERR%"=="0" (
    echo Package complete: project_packages\Project_For_ChatGPT.zip
) else (
    echo Package failed. Errorlevel: %ERR%
)

pause
exit /b %ERR%
