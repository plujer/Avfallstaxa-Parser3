# Block9 Hotfix – No Circular Import

Denna hotfix tar bort cirkulärt beroende.

Verifiera:

```bat
python -m pytest
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --context
python run.py --word "C:\PyProjects\data\Taxestruktur.docx" --semantic
```
