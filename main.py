from fastapi import FastAPI
from pydantic import BaseModel
from shuttle_logic import parse_event, validate_event

app = FastAPI()

class Event(BaseModel):
    Timestamp: str
    Route: str
    Bus: str
    Passengers: int
    Speed_kmh: int
    Status: str

def occupancy_category(passengers):
    if passengers <= 10:
        return "LOW"
    elif passengers <= 20:
        return "MEDIUM"
    elif passengers <= 30:
        return "HIGH"
    return "OVER_CAPACITY"

@app.post("/events")
def receive_event(event: Event):
    raw = event.model_dump()
    try:
        parsed = parse_event(raw)
    except (ValueError, KeyError, TypeError) as e:
        return {"result": "rejected", "errors": str(e), "occupancy_category": None}

    is_valid, reason = validate_event(parsed)
    if not is_valid:
        return {"result": "rejected", "errors": reason, "occupancy_category": None}

    return {
        "result": "accepted",
        "errors": None,
        "occupancy_category": occupancy_category(parsed["Passengers"]),
    }