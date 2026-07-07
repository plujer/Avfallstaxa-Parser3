@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM Excel Builder - Create Project Package for ChatGPT
REM Creates a compact ZIP without generated files, cache folders or virtual environments.
REM ==========================================

set PROJECT_ROOT=%~dp0
set OUTPUT=%PROJECT_ROOT%Project_For_ChatGPT.zip

if exist "%OUTPUT%" del "%OUTPUT%"

echo.
echo Creating compact project package for ChatGPT...
echo Output: %OUTPUT%
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$src='%PROJECT_ROOT%';" ^
"$dst='%OUTPUT%';" ^
"if(Test-Path $dst){Remove-Item $dst -Force};" ^
"$excludeDirs=@('.git','.venv','venv','__pycache__','.pytest_cache','output','rapportzip','dist','build','.mypy_cache','.ruff_cache','.idea','.vscode');" ^
"$excludeExt=@('.pyc','.pyo','.log','.tmp');" ^
"$files=Get-ChildItem $src -Recurse -File | Where-Object {" ^
"  $rel=$_.FullName.Substring($src.Length);" ^
"  $ok=$true;" ^
"  foreach($d in $excludeDirs){ if($rel -like ('*\'+$d+'\*')) { $ok=$false } };" ^
"  if($excludeExt -contains $_.Extension.ToLower()) { $ok=$false };" ^
"  $ok" ^
"};" ^
"$info=Join-Path $env:TEMP ('ExcelBuilder_PROJECT_INFO_' + [guid]::NewGuid().ToString() + '.txt');" ^
"'Excel Builder Project Package' | Out-File $info -Encoding UTF8;" ^
"('Created: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')) | Out-File $info -Encoding UTF8 -Append;" ^
"('Source: ' + $src) | Out-File $info -Encoding UTF8 -Append;" ^
"if(Test-Path (Join-Path $src 'version.json')){ 'version.json included' | Out-File $info -Encoding UTF8 -Append };" ^
"Compress-Archive -Path ($files.FullName + $info) -DestinationPath $dst -CompressionLevel Optimal;" ^
"Remove-Item $info -Force"

if exist "%OUTPUT%" (
    echo.
    echo ==========================================
    echo Package created successfully:
    echo %OUTPUT%
    echo ==========================================
) else (
    echo.
    echo FAILED to create package.
    echo ==========================================
    exit /b 1
)

pause
exit /b 0
