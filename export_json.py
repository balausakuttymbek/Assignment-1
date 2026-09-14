from data import raw_data
from shuttle_logic import event_generator
import json

def export_to_json(data_list, filename="sample_events.json"):
    results = []
    for item in event_generator(data_list):
        record = item["event"].copy()
        if hasattr(record.get("Timestamp"), "strftime"):
            record["Timestamp"] = record["Timestamp"].strftime("%H:%M")
        record["is_valid"] = item["is_valid"]
        record["reason"] = item["reason"]
        results.append(record)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results

export_to_json(raw_data)