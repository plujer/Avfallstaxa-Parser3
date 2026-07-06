# Changelog Block31

- Added row-level facit for §6.1.4.
- Added Section614Extractor for split El-kretsen/Hämtplatsportalen row.
- SemanticParser now combines the split §6.1.4 row before export.
- parser.py now writes reports directly to output subfolders.
- build_report.bat writes console/test/environment reports directly to output/diagnostics.
- Removed dependency on organize_output.py in build_report.bat to avoid Windows file-lock errors.
- Fixed syntax error in test_rapportzip_structure.py.
- Added tests for §6.1.4 facit and extraction.
