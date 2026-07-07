# Changelog Excel Builder Block 25

- Added DynamicTaxepunkterReader.
- MasterRuleRepositoryReader now uses WorkbookSchemaScanner indirectly through DynamicTaxepunkterReader.
- Fixed Taxepunkter reading when header row is not row 1.
- Added tests verifying Taxepunkter rules are extracted from row 5 headers.
