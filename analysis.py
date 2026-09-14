from data import raw_data
from shuttle_logic import event_generator


def analyze(data_list):
    total_passengers = 0
    count = 0
    max_passengers = None
    stopped_count = 0
    busiest_timestamp = None
    busiest_bus = None

    for item in event_generator(data_list):
        if not item["is_valid"]:
            continue
        event = item["event"]

        total_passengers += event["Passengers"]
        count += 1

        if event["Status"] == "STOPPED":
            stopped_count += 1

        if max_passengers is None or event["Passengers"] > max_passengers:
            max_passengers = event["Passengers"]
            busiest_timestamp = event["Timestamp"]
            busiest_bus = event["Bus"]

    return {
        "average_passengers": total_passengers / count,
        "max_passengers": max_passengers,
        "stopped_events": stopped_count,
        "busiest_minute": busiest_timestamp.strftime("%H:%M"),
        "busiest_bus": busiest_bus,
    }


if __name__ == "__main__":
    results = analyze(raw_data)
    for key, value in results.items():
        print(f"{key}: {value}")