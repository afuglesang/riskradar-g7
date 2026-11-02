# Risk Radar – G7 & EU

A daily, source-linked 30-day outlook of global security risks and national crisis risks for the G7 countries (United States, United Kingdom, France, Germany, Italy, Japan, Canada) and the European Union.

- `index.html` – the whole site (static, no build step). It reads `data/manifest.json` and `data/snapshots/YYYY-MM-DD.json`.
- `data/model.json` – the fixed structure: country list, factor IDs, outcome definitions and spill weights.
- `data/snapshots/` – one JSON file per day, written by the daily task.
- `tools/add_snapshot.py` – publishes one snapshot and updates the manifest.
- `ROUTINE-PROMPT.txt` – the instructions for the daily Claude Code routine.

## Method

Each factor has an analyst-assessed probability that its defined outcome happens within the next 30 days. Drivers move factors along a logistic curve, so changing a driver in the page shows how the factor and the overall risk respond.

- Global shock: P = 0.85 × [1 − (1 − 0.002) × Π(1 − P_factor × spill)].
- National crisis: the same formula with national and relevant global factors.

Probabilities are analytical judgements based on open sources. They are not forecasts or advice.

## Moving to a custom domain

1. Add a file `CNAME` with the domain, for example `riskradar.example.com`.
2. Point a DNS CNAME record at `afuglesang.github.io`.
3. Under Settings → Pages, set the custom domain and enable "Enforce HTTPS".
