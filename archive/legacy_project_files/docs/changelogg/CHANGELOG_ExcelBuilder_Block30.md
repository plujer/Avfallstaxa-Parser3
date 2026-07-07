# Changelog Excel Builder Block 30

- Added ParserTaxContext, ContextResolvedTaxRow and ContextResolutionReport models.
- Added ParserContextResolver.
- Added ContextResolutionReporter.
- Added excel_builder_context_resolve.py.
- Semantic decision CLI now uses context-resolved parser rows for semantic profiles.
- build_excel_report.bat now exports context resolution reports.
- Report ZIP includes context_resolution_report.txt and context_resolved_rows.csv.
- Added tests for inherited context and CLI packaging.
