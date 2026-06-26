# TrackFlow Incident Analysis API

Backend service exposing analysis and export endpoints for incident CSV files.

## Run

```bash
cd services/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Use port **8001** by default so this service does not conflict with other APIs on port 8000.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/analyze` | Upload CSV, returns analysis JSON |
| POST | `/export` | Upload CSV, returns metrics CSV download |

Docs: http://127.0.0.1:8001/docs
