Assignment 1 — Python Fundamentals for Data Streaming
AITU Campus Shuttle and Mobility Data. Synthetic educational dataset; does not
represent real AITU infrastructure, systems, or people.
Files
File	Purpose
`data.py`	Raw dataset (`raw_data`) — 10 shuttle events, Part A sample data
`shuttle_logic.py`	`parse_event()`, `validate_event()`, `event_generator()` — parsing, validation, and the streaming generator (Parts A & B)
`analysis.py`	`analyze()` — single-pass statistics over the validated stream (Part D)
`export_json.py`	Converts the dataset to `sample_events.json` via `event_generator()` (Part C)
`main.py`	FastAPI app; `POST /events` endpoint, `Event` request model, `occupancy_category()` (Part C)
`test_shuttle.py`	Pytest suite — 5 test functions, 13 cases total (Part E)
`notebook.ipynb`	Exploratory notebook covering Parts A and B
`sample_events.json`	Generated JSON sample (output of `export_json.py`)
Setup
```bash
pip install fastapi uvicorn pydantic pytest httpx
```
Run
Analysis (Part D):
```bash
python3 analysis.py
```
JSON export (Part C):
```bash
python3 export_json.py
# writes sample_events.json in the current directory
```
API server (Part C):
```bash
uvicorn main:app --reload
```
Then, in another terminal:
```bash
curl -X POST http://127.0.0.1:8000/events \
  -H "Content-Type: application/json" \
  -d '{"Timestamp":"08:09","Route":"AITU-Campus-Residence","Bus":"B02","Passengers":32,"Speed_kmh":24,"Status":"ON_ROUTE"}'
```
Tests (Part E):
```bash
python3 -m pytest test_shuttle.py -v
```
Design notes
`validate_event()` returns `(is_valid: bool, reason: str)` rather than
raising an exception — both the CLI/analysis path and the API path can
branch on the result without a try/except, and the reason string is
reused directly as the API's `errors` field.
`analyze()` iterates `event_generator()` once, keeping only running
totals (no intermediate list of events), so the same function would
still work unchanged against an unbounded stream.
`main.py` calls `parse_event()`/`validate_event()` from `shuttle_logic.py`
directly instead of duplicating validation rules in the Pydantic model —
one authoritative definition of "what is a valid event" for both the
streaming pipeline and the REST API.
Known limitation
`event_generator()` reads from an in-memory list (`raw_data`), not a real
external source (socket, growing log file, message queue). The constant-
memory property (see `stream_execution_evidence.txt`) holds for this input
shape, but isn't exercised at unbounded scale in this demo. A realistic
next step would be to swap `raw_data` for a generator that reads events
line-by-line from a file or queue.
