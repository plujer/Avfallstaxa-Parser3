# Install Block35 Final Test Escape Fix

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

Kör:

```bat
python -m pytest
build_report.bat
```

ZIP-filen för återrapportering finns i:

```text
rapportzip/
```

Commit:

```bat
git add .
git commit -m "Parser3 Block35 Final Test Escape Fix"
git push
```

När rapporten är helt grön kan vi göra `v1.0.0`-release.
