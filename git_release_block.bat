@echo off
setlocal

echo ==========================================
echo Excel Builder - git_release_block.bat
echo Block45 Developer Experience Test Automation
echo ==========================================
echo Kor endast nar ChatGPT sager att blocket ar releaseklart.
echo.

python tools\check_latest_run_status.py > output\diagnostics\latest_run_status.txt 2>&1
if errorlevel 1 (
    echo Release stoppad. Senaste teststatus ar inte godkand.
    type output\diagnostics\latest_run_status.txt
    pause
    exit /b 1
)

git status --porcelain > output\diagnostics\git_dirty_check.txt
for %%A in (output\diagnostics\git_dirty_check.txt) do if %%~zA NEQ 0 (
    echo Arbetskatalogen ar inte ren. Commit/pusha forst.
    type output\diagnostics\git_dirty_check.txt
    pause
    exit /b 1
)

git tag -a v1.0-block45 -m "Block45 Developer Experience Test Automation"
git push origin v1.0-block45

echo BLOCK45 RELEASE KLAR: v1.0-block45
pause
