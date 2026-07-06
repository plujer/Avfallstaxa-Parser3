# Changelog Excel Builder Block 21

- Added KnowledgeBasedStandardMatcher.
- StandardTaxSuggestionEngine now uses knowledge-based matching by default.
- Matching now weighs name, keywords, waste type, factor hint, category and unit.
- Standardtaxor remain suggestions only and never overwrite Taxa_från_edp.
- Added tests for knowledge-based standard matching.
