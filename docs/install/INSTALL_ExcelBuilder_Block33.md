# Install Excel Builder Block 33 – Build System Stabilization

Packa upp ZIP-filen i projektets rot och ersätt befintliga filer.

## Steg 1 – kontrollera status

```bat
git status
```

## Steg 2 – installera blocket

Packa upp ZIP-filen i projektroten och skriv över befintliga filer.

## Steg 3 – kontrollera specifikation

```bat
python tools\check_v1_spec.py
```

## Steg 4 – kör tester

```bat
python -m pytest
```

## Steg 5 – kör full rapportpipeline

```bat
build_excel_report.bat
```

## Steg 6 – skicka rapport

Skicka senaste filen från:

```text
rapportzip/
```

## Steg 7 – Git

```bat
git status
```

```bat
git add .
```

```bat
git status
```

```bat
git commit -m "Excel Builder Block33 Build System Stabilization"
```

```bat
git push
```

## Om något går fel innan commit

```bat
git restore .
```

## Om du redan hunnit göra commit men vill backa

```bat
git reset --soft HEAD~1
```
