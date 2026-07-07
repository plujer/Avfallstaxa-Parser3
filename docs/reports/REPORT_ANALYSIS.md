# REPORT_ANALYSIS – senaste analys

## Senaste rapport

```text
ExcelBuilder_Run_2026-07-07_10-37-44.zip
```

## Huvudresultat

Buildsystemet är stabilt igen efter Block33.

Full rapportpipeline körs och rapportzip innehåller alla centrala filer.

## Viktigaste kvarvarande problem

Rubriker och grupper skickas fortfarande till Decision Engine.

Exempel:

```text
En- och tvåbostadshus
Fritidshus
Verksamhet
```

Dessa ska bli `NOT_A_TAXA`, inte `NEW_TAXA`.

## Nästa rekommenderade block

```text
Block34 – Document Structure Engine
```

## Förväntad effekt

```text
färre falska NEW_TAXA
renare indata till semantik
mindre kontextläckage
bättre matchning
```
