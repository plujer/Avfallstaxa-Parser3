# Releasechecklista – Parser3 v1.0.0

## Före taggning

Kontrollera att senaste rapporten visar:

```text
Acceptance: 117/117
Pytest: 119 passed
```

## Git-kommandon

Kör från projektets rot:

```bat
git status
git add .
git commit -m "Release Parser3 v1.0.0"
git tag v1.0.0
git push
git push origin v1.0.0
```

## Efter taggning

Kontrollera:

```bat
git status
git tag
```

Förväntat:

```text
v1.0.0
```
