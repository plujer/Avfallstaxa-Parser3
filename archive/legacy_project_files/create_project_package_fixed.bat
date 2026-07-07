@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo.
echo Creating compact project package for ChatGPT...

set "PROJECT_ROOT=%~dp0"
set "OUTPUT=%PROJECT_ROOT%Project_For_ChatGPT.zip"
set "PS1=%TEMP%\create_project_package_%RANDOM%.ps1"

if exist "%OUTPUT%" del /f /q "%OUTPUT%" >nul 2>nul

> "%PS1%" echo $ErrorActionPreference = 'Stop'
>> "%PS1%" echo $src = "%PROJECT_ROOT%"
>> "%PS1%" echo $dst = "%OUTPUT%"
>> "%PS1%" echo $excludeDirs = @('.git','.venv','venv','__pycache__','.pytest_cache','output','rapportzip','dist','build','.mypy_cache','.ruff_cache','.idea','.vscode')
>> "%PS1%" echo $excludeExt = @('.pyc','.pyo','.log','.tmp')
>> "%PS1%" echo if (Test-Path $dst) { Remove-Item $dst -Force }
>> "%PS1%" echo $info = Join-Path $src 'PROJECT_INFO_FOR_CHATGPT.txt'
>> "%PS1%" echo "Excel Builder Project Package" ^| Out-File $info -Encoding UTF8
>> "%PS1%" echo "Created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" ^| Out-File $info -Append -Encoding UTF8
>> "%PS1%" echo "Root: $src" ^| Out-File $info -Append -Encoding UTF8
>> "%PS1%" echo try { "Git branch: $(git -C $src branch --show-current 2^> $null)" ^| Out-File $info -Append -Encoding UTF8 } catch {}
>> "%PS1%" echo try { "Git status:" ^| Out-File $info -Append -Encoding UTF8; git -C $src status --short ^| Out-File $info -Append -Encoding UTF8 } catch {}
>> "%PS1%" echo $files = Get-ChildItem $src -Recurse -File ^| Where-Object {
>> "%PS1%" echo     $full = $_.FullName
>> "%PS1%" echo     $rel = $full.Substring($src.Length).TrimStart('\')
>> "%PS1%" echo     if ($rel -eq 'Project_For_ChatGPT.zip') { return $false }
>> "%PS1%" echo     foreach ($d in $excludeDirs) {
>> "%PS1%" echo         if ($rel -like "$d\*" -or $rel -like "*\$d\*") { return $false }
>> "%PS1%" echo     }
>> "%PS1%" echo     if ($excludeExt -contains $_.Extension.ToLower()) { return $false }
>> "%PS1%" echo     return $true
>> "%PS1%" echo }
>> "%PS1%" echo Compress-Archive -Path $files.FullName -DestinationPath $dst -CompressionLevel Optimal -Force
>> "%PS1%" echo Remove-Item $info -Force -ErrorAction SilentlyContinue
>> "%PS1%" echo Write-Host "Package created: $dst"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
set "ERR=%ERRORLEVEL%"
del /f /q "%PS1%" >nul 2>nul

if "%ERR%"=="0" (
    echo.
    echo ==========================================
    echo Project package created:
    echo %OUTPUT%
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo FAILED to create project package.
    echo Errorlevel: %ERR%
    echo ==========================================
)

pause
exit /b %ERR%
