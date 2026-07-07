@echo off
setlocal
echo ==========================================
echo Git release - Block44
echo ==========================================
echo Kontrollera att Block44 är godkänt innan du fortsätter.
git status
git tag -a v1.0-block44 -m "Block44 immutable master enforcement verified"
git push
git push origin v1.0-block44
pause
endlocal
