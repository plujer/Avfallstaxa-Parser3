# Block 19 – Facit YAML 6.1.2

Detta block gör `parser_facit.yaml` till officiell facitkälla för acceptance-test.

§6.1.2 innehåller nu:
- Block A: 26 taxor
- Block B: 63 taxor
- Block C: 14 taxor
- Totalt: 103 taxor
- 1 hänvisning som inte ska exporteras

Arbets-Excel är fortfarande inte facit.

Kör:

```bat
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic --acceptance-debug
python -m pytest
build_report.bat
```
