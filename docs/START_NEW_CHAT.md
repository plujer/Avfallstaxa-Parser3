Detta är en fortsättning på projektet Excel Builder.

Jag har laddat upp följande filer:

- ExcelBuilder_Project_Handover_v0.9.3.zip
- ExcelBuilder_Master_v0.9.4_Handover.zip
- senaste rapportzip från rapportzip/
- (eventuellt senaste standardtaxefilen om den har ändrats)

Arbeta enligt dokumentationen i handover-paketet.

Börja med att läsa och sammanfatta följande dokument innan du skriver någon kod:

1. docs/00_START_HERE.md
2. docs/PROJECT_STATUS.md
3. docs/SPECIFICATION.md
4. docs/ROADMAP.md
5. docs/PROJECT_RULES.md
6. docs/PROJECT_MEMORY.md
7. docs/ARCHITECTURE.md
8. docs/CHANGELOG.md
9. docs/history/BLOCK_HISTORY.md
10. senaste rapportzip

Använd dessutom den nya masterarbetsboken:

data/master_templates/ArbetsExcel_Template_v0.9.4_draft.xlsx

Den ersätter den tidigare ArbetsExcel_Reference.xlsx och ska användas som projektets master från och med nu.

Viktiga regler:

- Taxa_från_edp är alltid facit och får aldrig ändras automatiskt.
- Standardtaxor används endast som beslutsstöd och förslag.
- Kommunprojekten Sorsele, Malå och Norsjö ska alltid hållas helt separata.
- Kunskap delas, kommununik data delas inte.
- Masterarbetsboken är versionsstyrd och får inte ändras utan godkännande. Om en ändring behövs ska en ny versionsbaserad master skapas.
- Efter varje utvecklingsblock ska arbetsrutinen i PROJECT_MEMORY.md följas.
- Inga nya funktioner får utvecklas innan föregående block är verifierat med tester, rapportzip och uppdaterad dokumentation.

Jag vill att du först verifierar att du förstått projektet genom att sammanfatta:

1. Projektets mål.
2. Projektets arkitektur.
3. Nuvarande status.
4. De viktigaste reglerna.
5. De tre högst prioriterade nästa utvecklingsstegen.

Börja inte skriva kod förrän denna analys är klar.

När analysen är godkänd fortsätter vi med nästa planerade utvecklingsblock enligt ROADMAP.md, vilket förväntas vara Block34 – Document Structure Engine.

Vid varje nytt block vill jag att du alltid levererar:

- tydlig beskrivning av syfte,
- vilka filer som ändras,
- installationsinstruktioner,
- testinstruktioner,
- Git-kommandon,
- vad jag ska skicka tillbaka efter körning,
- samt uppdateringar till PROJECT_STATUS, CHANGELOG och BLOCK_HISTORY om blocket godkänns.