# MASTER_SETUP_INSTRUCTIONS – använd v0.9.4 som ny master

## Syfte

Den nya filen:

```text
data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx
```

ska från och med nu användas som projektets masterarbetsbok.

Den ersätter den äldre:

```text
data/ArbetsExcel_Reference.xlsx
```

## Steg 1 – Packa upp ZIP-filen

Packa upp hela innehållet i projektets rotmapp.

Efter uppackning ska du ha:

```text
data/
└── master_templates/
    ├── ArbetsExcel_Template_v0.9.4_draft.xlsx
    └── VERSION_HISTORY.md
```

## Steg 2 – Behåll gärna gamla filen, men använd den inte som aktiv master

Du kan låta gamla filen ligga kvar som historik, men aktiv master ska vara:

```text
data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx
```

## Steg 3 – I nya chatten

Ladda upp denna ZIP tillsammans med projektöverlämningen:

```text
ExcelBuilder_Master_v0.9.4_Handover.zip
ExcelBuilder_Project_Handover_v0.9.3.zip
senaste rapportzip
```

Skriv i nya chatten att denna master ska användas som ny referens.

## Steg 4 – Kommande kodändring

I nästa utvecklingsblock bör script som idag använder:

```text
data/ArbetsExcel_Reference.xlsx
```

ändras till:

```text
data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx
```

Det bör göras kontrollerat i Block34 eller ett separat master-path block.

## Viktiga regler

```text
Taxa_från_edp är fortfarande facit.
Masterfilen är draft och får inte låsas som v1.0 ännu.
Nya ändringar i master kräver ny versionsfil.
```
