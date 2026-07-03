# Parser 3.0 Architecture

Parser 3.0 ska byggas som en radbaserad dokumentmotor.

## Flöde

1. DocumentReader
2. HeadingTreeBuilder
3. SmartTableDetector
4. RowClassifier
5. TaxRowExtractor
6. MetadataExtractor
7. ValidationEngine
8. ExcelExporter

## Grundprincip

Parsern får inte anta att varje tabellrad är en taxa. Varje rad ska klassificeras först.
