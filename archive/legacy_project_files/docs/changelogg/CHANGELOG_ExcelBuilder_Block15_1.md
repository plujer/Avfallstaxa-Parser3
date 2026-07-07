# Changelog Excel Builder Block 15.1

- Fixed report ZIP regression: standard tax source workbook is included again.
- Added `EDP_Avviker_Standard` sheet to generated workbooks.
- Documented fixed EDP rule in generated `Körningsinfo`.
- Added tests to ensure standardtaxor cannot overwrite existing `Taxa_från_edp`.
- No automatic EDP overwrite logic added.
