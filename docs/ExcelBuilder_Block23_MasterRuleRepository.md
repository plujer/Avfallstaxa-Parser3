# Excel Builder Block 23 – Master Rule Repository

Detta block börjar använda masterarbetsboken som regelkälla.

## Prioriteringsordning

1. Läs in hela masterarbetsboken.
2. Bygg internt Rule Repository.
3. Låt Knowledge Index och matchningsmotorn kunna använda detta senare.
4. Standardtaxor används som kompletterande källa.

## Nya delar

```text
MasterRuleRepositoryReader
RuleRepositoryReporter
excel_builder_rule_repository.py
```

## Nya rapporter

```text
output/excel/master_rule_repository_report.txt
output/excel/master_rule_repository.csv
```

## Viktigt

Masterarbetsboken läses endast.

Den ändras inte automatiskt.

## Kör tester

```bat
python -m pytest
```

## Bygg rapportpaket

```bat
build_excel_report.bat
```

## Skicka tillbaka

```text
rapportzip/
```
