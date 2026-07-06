# Install Block33 Release Cleanup

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python -m pytest
build_report.bat
```

ZIP-filen för återrapportering finns därefter i:

```text
rapportzip/
```

Commit:

```bat
git add .
git commit -m "Parser3 Block33 Release Cleanup"
git push
```

Gör **inte** v1.0.0-taggen förrän rapporten visar att allt är grönt.
