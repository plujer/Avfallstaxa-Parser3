# Changelog Block20

- Added NameNormalizer for acceptance comparison.
- AcceptanceRunner and AcceptanceDebugger now use NameNormalizer.
- Added Section612Extractor for §6.1.2 rows without explicit price markers.
- SemanticParser now uses Section612Extractor for non-tax rows in §6.1.2.
- Added deduplication of semantic tax rows.
- Added tests for aliases and §6.1.2 Block A extraction.
