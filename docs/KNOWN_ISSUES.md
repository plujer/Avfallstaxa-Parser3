# KNOWN_ISSUES – Excel Builder

## 1. Rubriker blir ibland NEW_TAXA

Exempel:

```text
En- och tvåbostadshus
Fritidshus
Verksamhet
Lägenhet i flerbostadshus
```

Dessa ska klassas som `NOT_A_TAXA`.

Planerad lösning:

```text
Block34 – Document Structure Engine
```

## 2. Context Resolver kan läcka kontext

Exempel från tidigare analys:

```text
Extra digital licens
```

fick felaktigt kontext från tidigare avsnitt.

Planerad lösning:

```text
Block35 – Hierarchical Context Resolver
```

## 3. Taxefamiljer används inte fullt ut

Taxekoder är tolkade men familjer används ännu inte fullt ut i beslut.

Planerad lösning:

```text
Block36 – Tax Family Intelligence
```

## 4. Rule Repository innehåller brus

Regler utan taxekod kan konkurrera med riktiga kandidater.

Planerad lösning:

```text
Block37 – Rule Repository Cleanup
```

## 5. EDP Export Builder saknas

Det finns ännu inget slutligt exportflöde tillbaka till EDP.

Planerad lösning:

```text
Block39 – EDP Export Builder Preview
```
