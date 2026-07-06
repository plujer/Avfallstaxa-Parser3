# Changelog Block25

- Section612Extractor now prefers exact matches, then longest substring matches, then fuzzy matches.
- Fixed the short-substring bug where `Avfall till energiåtervinning` could win over the longer skrymmande-row.
- NameNormalizer no longer removes generic four-digit numbers, only EWC-style six-digit codes.
- Added regression tests for the final §6.1.2 specific-match issue.
