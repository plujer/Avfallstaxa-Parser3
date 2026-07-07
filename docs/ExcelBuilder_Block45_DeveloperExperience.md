# Block45 – Developer Experience Test Automation

Syfte:
- `run_project.bat` kör hela pipeline och därefter hela pytest-sviten automatiskt.
- Blocket återställer rapportstegen för Tax Family, Variant, Semantic Attributes, Composite Matching och Explainable Decision som saknades i Block44-körningen.
- `git_commit_block.bat` blockerar commit om senaste pytest-körningen inte är godkänd.
- Rapportzip innehåller pytest-status och relevanta master-/guard-rapporter.

Regel om dubbletter:
Samma Word-rad eller paragrafrad kan legitimt kopplas till samma EDP-taxa. Det är inte automatiskt ett fel. Fel ska endast flaggas när kopplingen är motstridig eller bryter mot Taxa_från_edp som facit.
