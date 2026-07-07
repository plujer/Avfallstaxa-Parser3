# ARCHITECTURE – Excel Builder

## Översikt

```text
Word
  ↓
Parser
  ↓
Document Structure Engine
  ↓
Tax Node Extractor
  ↓
Hierarchical Context Resolver
  ↓
Tax Semantic Profile Engine
  ↓
Semantic Candidate Ranking
  ↓
Semantic Decision Engine
  ↓
Excel Builder
  ↓
Kommununik ArbetsExcel
  ↓
EDP Export Builder
```

## Centrala moduler

### Parser

Läser Word och skapar parserrader.

### Document Structure Engine

Planerad från Block34.

Ska skilja rubriker, grupper, tabeller och verkliga taxor.

### Context Resolver

Berikar taxor med kontext.

Nuvarande version är rullande. Nästa version ska bli hierarkisk.

### Tax Code Intelligence

Tolkar taxekoder som:

```text
KÄ240RM26FV
```

till:

```text
Kärl
240 L
RM
26
FV
```

### Rule Repository

Byggs från masterarbetsboken.

Innehåller:

```text
Taxepunkter
Taxa_från_edp
dokumentation
standardreferenser
```

### Semantic Candidate Ranking

Poängsätter kandidater från:

```text
kommunens EDP
Taxepunkter
standardtaxor
regelrepository
```

### Semantic Decision Engine

Skapar beslut:

```text
EDP_MATCH
STANDARD_PROPOSAL
RULE_PROPOSAL
REVIEW_REQUIRED
NEW_TAXA
NOT_A_TAXA
```

### Excel Builder

Skapar färdig arbetsbok från masterkopia.

## Kommunisolering

```text
output/projects/Sorsele/
output/projects/Mala/
output/projects/Norsjo/
```

Varje kommun ska ha egen körning och egen output.
