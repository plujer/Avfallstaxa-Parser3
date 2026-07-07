# GIT_WORKFLOW – Excel Builder

## Före varje block

```bat
git status
```

Målet är helst:

```text
nothing to commit, working tree clean
```

## Installera nytt block

Packa upp ZIP-filen i projektroten och skriv över filer.

## Kör kontroller

```bat
python tools\check_v1_spec.py
```

```bat
python -m pytest
```

```bat
build_excel_report.bat
```

## Efter godkänd körning

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
git commit -m "BlockXX - Kort beskrivning"
```

```bat
git push
```

## Skapa tagg vid stabil version

```bat
git tag v0.9.3-build-stable
```

```bat
git push origin v0.9.3-build-stable
```

## Om något går fel före commit

Återställ ändringar:

```bat
git restore .
```

Ta bort nya filer som inte spåras:

```bat
git clean -fd
```

Varning: `git clean -fd` tar bort ospårade filer.

## Om du redan commitat men vill göra om

Behåll filerna men ta bort senaste commit:

```bat
git reset --soft HEAD~1
```

## Om du måste backa helt

```bat
git reset --hard HEAD~1
```

Varning: tar bort ändringar permanent om de inte finns sparade.
