# ExcelBuilder Block50 – Word Excel Mapping 2.0

## Syfte

Block50 stärker Word → Excel-spårbarheten genom att varje Word-taxarad får två identiteter:

- `WordTaxID`: sectionsbundet ID för exakt spårning i aktuell Word-master.
- `StableTaxIdentity`: sectionsoberoende innehålls-ID som kan känna igen samma taxepunkt även om den flyttas till annan paragraf i Word.

## Regler

- Word-mastern ändras aldrig.
- Excel-mastern ändras aldrig.
- `Taxepunkter!A:E` ändras aldrig automatiskt.
- `Taxa_från_edp` ändras aldrig.
- Samma EDP-taxa kan vara kopplad till flera Word-rader utan att det automatiskt är fel.

## Output

- `output/excel/word_excel_mapping_report.txt`
- `output/excel/word_excel_mapping.csv`

CSV-filen innehåller nu kolumnerna `StableTaxIdentity` och `ContentFingerprint`.
