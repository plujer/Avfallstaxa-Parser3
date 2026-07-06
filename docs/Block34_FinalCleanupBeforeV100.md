# Block 34 – Final Cleanup Before v1.0.0

Detta är ett rent cleanup-block innan riktig release/taggning.

## Vad senaste rapporten visade

- Acceptance: 117/117
- Pytest: 116 passed
- Parsern är funktionsmässigt klar för v1.0.0

## Fix i detta block

`tools/zip_output.ps1` zippar inte längre `output/archive/`.

Tidigare kunde gamla ZIP-filer råka packas in i nya ZIP-filer, vilket gör att rapportpaketen växer snabbt.

Nu packas endast dessa mappar:

```text
output/acceptance
output/diagnostics
output/trace
output/reports
output/excel
output/word
```

En arkivkopia skapas fortfarande i:

```text
output/archive/
```

## Kör

```bat
python -m pytest
build_report.bat
```

När rapporten visar grönt kan vi göra riktiga `v1.0.0`-releasen.
