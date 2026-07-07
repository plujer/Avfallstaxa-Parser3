@echo off
setlocal
echo ==========================================
echo Git release - Block43
echo ==========================================
echo Kör endast när blocket är godkänt som releasepunkt.
git status --porcelain > %TEMP%\git_status_block43.txt
for %%A in (%TEMP%\git_status_block43.txt) do if %%~zA neq 0 (
    echo Arbetskatalogen är inte ren. Kör commit först.
    type %TEMP%\git_status_block43.txt
    pause
    exit /b 1
)
git tag -a v1.0-block43 -m "Block43 Master Source Integration verified"
git push
git push origin v1.0-block43
pause
endlocal
