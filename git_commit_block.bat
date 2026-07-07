@echo off
setlocal
echo ==========================================
echo Git commit - Block44
echo ==========================================
git status
git add excel_builder\guards
git add tools\check_immutable_master_enforcement.py
git add build_excel_report.bat
git add run_project.bat run_tests.bat run_reports.bat run_clean.bat git_commit_block.bat git_release_block.bat
git add tests\test_immutable_master_enforcement.py
git add docs\PROJECT_RULES.md docs\PROJECT_STATUS.md docs\CHANGELOG.md docs\history\BLOCK_HISTORY.md
git commit -m "Block44: Enforce immutable master templates"
git status
pause
endlocal
