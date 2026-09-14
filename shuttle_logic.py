import re
from datetime import datetime


def parse_event(event_dict):
    parsed = event_dict.copy()
    parsed["Timestamp"] = datetime.strptime(event_dict["Timestamp"], "%H:%M").time()
    parsed["Passengers"] = int(event_dict["Passengers"])
    parsed["Speed_kmh"] = int(event_dict["Speed_kmh"])
    return parsed


def validate_event(event_dict):
    if event_dict["Passengers"] < 0:
        return False, "Passengers cannot be negative"
    if not (0 <= event_dict["Speed_kmh"] <= 120):
        return False, "Speed must be between 0 and 120 km/h"
    if event_dict["Status"] not in ["ON_ROUTE", "STOPPED"]:
        return False, "Invalid status"
    return True, "Valid"


def event_generator(data_list):
    for item in data_list:
        try:
            parsed_item = parse_event(item)
        except (ValueError, KeyError, TypeError) as e:
            yield {"event": item, "is_valid": False, "reason": f"Parse error: {e}"}
            continue

        is_valid, reason = validate_event(parsed_item)
        yield {"event": parsed_item, "is_valid": is_valid, "reason": reason}