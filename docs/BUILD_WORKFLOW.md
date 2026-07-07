# BUILD_WORKFLOW – Excel Builder

## Full pipeline

Kör:

```bat
build_excel_report.bat
```

Den ska göra:

```text
1. Kontrollera v1.0-specifikation
2. Rensa testdubbletter
3. Kontrollera testsyntax
4. Köra pytest
5. Lösa parserkontext
6. Scanna masterarbetsbok
7. Scanna standardtaxekatalog
8. Tolka taxekoder
9. Extrahera Tax Knowledge
10. Bygga Knowledge Index
11. Bygga semantiska profiler
12. Rankar semantiska kandidater
13. Profilerar arbetsboken
14. Läser EDP-regelverk
15. Bygger Master Rule Repository
16. Skapar snapshot
17. Bygger Taxepunkter row plan
18. Kör matching preview
19. Skapar standardtaxeförslag
20. Bygger Arbets-Excel
21. Skriver Tax Knowledge
22. Skriver standardförslag
23. Kör gammal beslutsmotor som jämförelse
24. Kör semantisk beslutsmotor
25. Kör coverage
26. Kör Sorsele-projekt
27. Skapar rapportzip
```

## Rapport som ska skickas till ChatGPT

Skicka senaste filen från:

```text
rapportzip/
```

## Viktigt

Om buildfilen förenklas och rapporterna försvinner ska det räknas som regression.
