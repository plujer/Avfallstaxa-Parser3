# Excel Builder v1.0 – roadmap

## Fas 1 – Plattform

Status: i princip klar.

```text
Parser
Excel Builder
EDP-import
Standardtaxor
Masterkopiering
Kommunisolering
Rule Repository
Semantic Profiles
Candidate Ranking
Semantic Decision Engine
Rapportpaket
Testsvit
```

## Fas 2 – Domänintelligens

Status: påbörjad.

### Steg A – Document Structure Engine

Mål:

```text
skilja rubriker från taxor
skapa dokumentträd
bara skicka taxenoder vidare till beslut
```

Förväntad effekt:

```text
färre falska NEW_TAXA
mindre kontextläckage
bättre Word-förståelse
```

### Steg B – Hierarkisk Context Resolver

Mål:

```text
ärva kontext inom dokumentgren
nollställa kontext vid nytt avsnitt
tolka underförstådda egenskaper
```

### Steg C – Tax Family Intelligence

Mål:

```text
gruppera taxekoder i familjer
identifiera varianter
föreslå saknade familjemedlemmar
```

### Steg D – Rule Repository Cleanup

Mål:

```text
markera regler utan taxekod
ta bort dubbletter från kandidatpoolen
behålla dem som dokumentationsstöd
```

### Steg E – Decision Engine 2.0

Mål:

```text
använda dokumentstruktur
använda taxefamiljer
visa bättre confidence
visa varför kandidaten valdes
```

## Fas 3 – Slutflöde

### EDP Export Builder

Mål:

```text
skapa ny exportstruktur
separera nya, ändrade och oförändrade taxor
säker import tillbaka till EDP
```

### Rule Learning

Mål:

```text
spara manuella korrigeringar som generell kunskap
inte blanda kommunprojekt
versionera kunskapen
```

## Rekommenderad ordning från nu

```text
Block 33 – Document Structure Engine
Block 34 – Hierarchical Context Resolver
Block 35 – Tax Family Intelligence
Block 36 – Rule Repository Cleanup
Block 37 – Decision Engine 2.0
Block 38 – EDP Export Builder Preview
Block 39 – Knowledge Versioning
Block 40 – v1.0 Release Hardening
```
