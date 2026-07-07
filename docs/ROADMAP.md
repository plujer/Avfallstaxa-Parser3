# ROADMAP – Excel Builder

## Senaste klara block

```text
Block33 – Build System Stabilization
```

## Nästa block

```text
Block34 – Document Structure Engine
```

## Rekommenderad ordning

### Block34 – Document Structure Engine

Bygg dokumentträd och separera:

```text
SECTION
SUBSECTION
TABLE_HEADER
TABLE_ROW
TAX_NODE
NOTE
```

Endast `TAX_NODE` ska gå vidare till semantik och beslut.

### Block35 – Hierarchical Context Resolver

Ersätt rullande kontext med hierarkisk kontext.

Kontext ska ärvas inom rätt dokumentgren och nollställas vid nytt avsnitt.

### Block36 – Tax Family Intelligence

Använd taxekodsfamiljer, exempel:

```text
KÄ240RM
    26
    52
    104
    FV
    FRI
```

### Block37 – Rule Repository Cleanup

Filtrera bort eller nedprioritera regler utan taxekod i kandidatpoolen.

De får finnas kvar som dokumentation, men ska inte konkurrera med riktiga taxekoder.

### Block38 – Decision Engine 2.0

Använd dokumentstruktur, taxefamiljer och förbättrad confidence.

### Block39 – EDP Export Builder Preview

Skapa preliminär exportstruktur för ny/kompletterad EDP-import.

### Block40 – Knowledge Versioning

Inför versionerad kunskapsdatabas:

```text
data/knowledge/v1/
```

### Block41 – v1.0 Release Hardening

Rensa varningar, stabilisera tester, dokumentera release.
