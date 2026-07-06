# Installationsinstruktioner – Parser3 v1.0.0

## 1. Säkerhetskopiera projektet
Skapa en kopia av projektmappen eller skapa en Git-tag innan installation.

## 2. Packa upp releasen
Packa upp innehållet i projektets rot och välj **Ersätt befintliga filer**.

## 3. Kör verifiering

```bat
python -m pytest
build_report.bat
```

## 4. Kontrollera resultat

Acceptance ska visa:

- §6.1.1 = 6/6
- §6.1.2 = 103/103
- §6.1.3 = 4/4
- §6.1.4 = 4/4

Totalt:

```
117 / 117
Passed: True
```

ZIP-filen för återrapportering skapas i:

```
rapportzip/
```

## 5. Git

```bat
git add .
git commit -m "Release Parser3 v1.0.0"
git tag v1.0.0
git push
git push origin v1.0.0
```
