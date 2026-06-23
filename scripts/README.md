# `scripts` folder

This folder contains **helper scripts** for the monorepo: development automation, maintenance utilities, repetitive tasks (setup, lint, migrations, data generation, etc.), and internal tooling.

- **Main purpose**: group support tools that do not belong to a specific app, agent, or pipeline but make the team’s work easier.
- **Recommendation**: document each script (what it does, parameters, requirements, usage examples) and keep them reproducible (and safe) across environments.

> _Spanish version: [README.es.md](./README.es.md)._

## `seed_incidents.py`

Loads historical incidents from a CSV file into the backoffice incident store.

- Reuses a centralized incident schema for required fields and allowed values.
- Forces `origin` to `customer` for imported historical records.
- Is idempotent through a deterministic fingerprint (`--id-columns`) to avoid duplicates.
- Reports invalid rows at the end of execution.

Example:

```bash
python3 scripts/seed_incidents.py \
	--csv-path data/raw/incidents_history.csv \
	--data-path uis/backoffice/data/incidents.json \
	--id-columns title,description,category,branch
```
