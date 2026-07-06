# Block 17 – Parser Acceptance

Detta block verifierar parsern mot det facit vi manuellt har godkänt.

## Viktigt

Detta jämför **inte** mot Arbets-Excel som facit.

Worddokumentet och manuellt verifierade sektionsregler är facit.

## Inbyggt verifierat facit

- 6.1.1 = 6 taxor
- 6.1.2 = 103 taxor
- 6.1.3 = 4 taxor
- 6.1.4 = 4 taxor

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance
```

eller kör hela paketet:

```bat
build_report.bat
```

Rapport:

```text
output\parser3_acceptance_report.txt
```
