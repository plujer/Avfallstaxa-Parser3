# SPECIFICATION – Excel Builder v1.0

## Målbild

Excel Builder v1.0 ska kunna köra ett komplett flöde:

```text
Word
+
EDP-export
+
Masterarbetsbok
        ↓
Färdig kommununik Excel-arbetsbok
        ↓
Beslutsrapporter
        ↓
Förslag till EDP-export/import
```

## Orubbliga principer

### Kommunens EDP är facit

```text
Taxa_från_edp får aldrig ändras automatiskt.
Taxor som redan finns i Taxa_från_edp är fasta.
```

### Standardtaxor är endast förslag

```text
Standardtaxor får användas som beslutsstöd.
Standardtaxor får inte skriva över kommunens befintliga EDP-taxor.
```

### Masterarbetsboken är mall och regelkälla

```text
Masterarbetsboken ska kopieras.
Kopian ska fyllas.
Originalmaster får inte ändras automatiskt.
```

### Masterändringar kräver godkännande

Om ny kolumn, flik, formel eller struktur behövs:

```text
1. Föreslå ändringen.
2. Invänta godkännande.
3. Skapa ny versionerad master.
4. Dokumentera ändringen.
```

### Kunskap delas – data delas inte

Delas globalt:

```text
taxekodsmönster
taxefamiljer
semantiska regler
standardtaxelogik
generella inlärda regler
```

Delas inte:

```text
Sorseles EDP-export
Malås EDP-export
Norsjös EDP-export
kommununika beslut
kommununika arbetsböcker
```

## Obligatoriska beslutsstatusar

```text
EDP_MATCH
STANDARD_PROPOSAL
RULE_PROPOSAL
REVIEW_REQUIRED
NEW_TAXA
NOT_A_TAXA
```

## Acceptanskriterier v1.0

```text
Alla tester passerar.
Full rapportzip skapas efter varje körning.
Kommunprojekt hålls isolerade.
Taxa_från_edp ändras inte automatiskt.
Alla Word-taxor finns i Taxepunkter.
Rubriker klassas inte som NEW_TAXA.
Beslut har confidence och motivering.
Master är versionsstyrd.
EDP-export kan byggas som underlag.
```
