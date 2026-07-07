# DECISION_LOG – Excel Builder

## Beslut 1 – Taxa_från_edp är facit

Befintliga EDP-taxor ska aldrig ändras automatiskt.

Motiv:

```text
EDP är kommunens faktiska källa.
Felaktig ändring kan skapa importproblem.
```

## Beslut 2 – Standardtaxor är endast förslag

Standardtaxor används för att hitta saknade taxor och ge förslag.

De får inte skriva över kommunens taxor.

## Beslut 3 – Masterarbetsboken är mall och regelkälla

Systemet ska kopiera master och fylla kopian.

Master får inte ändras direkt.

## Beslut 4 – Kommunisolering

Sorsele, Malå och Norsjö ska vara separata projekt.

Generell kunskap får återanvändas, men kommununik data får inte blandas.

## Beslut 5 – Buildpipeline ska alltid vara fullständig

Block32 visade att en förenklad buildfil skapade regression.

Därför finns nu stabiliseringstest i Block33.

## Beslut 6 – Nästa stora steg är dokumentstruktur

Rapporter visar att rubriker ibland klassas som taxor.

Därför prioriteras Document Structure Engine före fler beslutströsklar.
