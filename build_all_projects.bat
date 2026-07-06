@echo off
setlocal

echo ==========================================
echo Excel Builder Project - Alla kommuner
echo ==========================================

python excel_builder_project_run.py --config "data\projects\Mala\project_config.json"
python excel_builder_project_run.py --config "data\projects\Norsjo\project_config.json"
python excel_builder_project_run.py --config "data\projects\Sorsele\project_config.json"

echo.
echo KLAR
echo Output finns i output\projects\Mala, output\projects\Norsjo och output\projects\Sorsele
echo ==========================================

pause
endlocal
