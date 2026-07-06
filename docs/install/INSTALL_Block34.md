# Install Block34 Final Cleanup Before v1.0.0

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
git commit -m "Parser3 Block34 Final Cleanup Before v1.0.0"
git push
```

Vänta med `git tag v1.0.0` tills rapporten efter detta block är grön.
