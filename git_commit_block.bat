@echo off
setlocal
echo ==========================================
echo Git commit - Block43
echo ==========================================
git status
git add config\master_sources.json
git add data\master_templates\ArbetsExcel_Template_v1.0.xlsx
git add data\word_templates\Taxestruktur_Master_v1.0.docx
git add excel_builder\config
git add excel_builder\guards
git add excel_builder\template\template_master_manager.py
git add excel_builder\io\workbook_writer.py
git add tools\check_master_sources.py
git add tools\zip_excel_report.ps1
git add build_excel_report.bat build_excel.bat parser3\build_excel_report.bat
git add run_project.bat run_tests.bat run_reports.bat run_clean.bat git_commit_block.bat git_release_block.bat
git add tests\test_master_source_integration.py tests\test_excel_builder_writer.py tests\test_template_master_manager.py
git add docs\PROJECT_RULES.md docs\PROJECT_STATUS.md docs\CHANGELOG.md docs\history\BLOCK_HISTORY.md
git commit -m "Block43: Integrate immutable master sources v1.0"
git status
pause
endlocal
