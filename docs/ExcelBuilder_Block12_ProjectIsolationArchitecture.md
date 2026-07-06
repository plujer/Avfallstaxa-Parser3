# Excel Builder Block 12 – Project Isolation Architecture

Detta block inför projektarkitekturen.

## Grundprincip

```text
Ett projekt = en Wordfil + en EDP-export + ett outputområde
```

Projektdata får inte blandas mellan kommuner.

## Isolerade projekt

```text
data/projects/Sorsele/project_config.json
data/projects/Mala/project_config.json
data/projects/Norsjo/project_config.json
```

Varje projekt pekar på en egen EDP-export:

```text
data/edp_exports/Sorsele.xlsx
data/edp_exports/Mala.xlsx
data/edp_exports/Norsjo.xlsx
```

## Output

```text
output/projects/Sorsele/
output/projects/Mala/
output/projects/Norsjo/
```

## Nya kommandon

### Kör bara Sorsele

```bat
build_sorsele_project.bat
```

### Kör alla projekt

```bat
build_all_projects.bat
```

### Bygg rapportpaket

```bat
build_excel_report.bat
```

## Viktigt

- Sorsele EDP används bara i Sorsele-projektet.
- Malå EDP används bara i Malå-projektet.
- Norsjö EDP används bara i Norsjö-projektet.
- Generella regelverk får återanvändas.
