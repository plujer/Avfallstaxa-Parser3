# Block4 Hotfix EWC v2

Packa upp ZIP-filen i projektets rot och välj att ersätta befintliga filer.

Viktigt:
- Denna hotfix ersätter `parser3/extractors/metadata_extractor.py`
- Den ersätter även `tests/test_tax_extractor.py`

Verifiera:

```bat
python -m pytest
```

Snabb kontroll av filen:

```bat
type parser3\extractors\metadata_extractor.py
```

Commit:

```bat
git add .
git commit -m "Fix EWC star metadata extraction"
git push
```
