# Changelog Block14

- Added official TaxPipeline.
- Added PipelineReporter.
- Added FlatTaxExtractor for visual table rows.
- CLI now routes semantic/diff/export through TaxPipeline.
- TaxRowExtractor delegates single-cell rows to FlatTaxExtractor.
- Added tests for flat visual rows and pipeline flow.
