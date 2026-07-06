# Block 18 – Acceptance Debug

Detta block hittar exakt vilka manuellt verifierade facitrader som saknas.

## Viktigt

Detta är fortfarande verifiering av parsern mot Word/facit.
Det använder inte Arbets-Excel som facit.

## Kör

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance-debug
```

eller:

```bat
build_report.bat
```

## Ny rapport

```text
output\parser3_acceptance_debug_report.txt
```

Rapporten visar per sektion:

- missing names
- extra exported
- possible parser names
- om saknade namn finns i semantic rows men inte exporterades
