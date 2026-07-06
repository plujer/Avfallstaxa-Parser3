# Changelog Block24

- Added trace module with TraceEvent, TraceStore and TraceReporter.
- Section612Extractor now records export/not_export decisions.
- SemanticParser and TaxPipeline now expose trace_store.
- Added --trace CLI flag.
- build_report.bat now includes --trace.
- ZIP output now includes parser3_trace_report.txt.
- Added tests for Section612Extractor trace decisions.
