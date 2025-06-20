import requests
import json

API_BASE = "https://v6.vbb.transport.rest"

def get_station_id(name):
    response = requests.get(f"{API_BASE}/locations", params={"query": name, "results": 1})
    if response.ok:
        data = response.json()
        if data and 'id' in data[0]:
            return data[0]['id']
    return None

def fetch_journeys(origin_name, destination_name, time="now"):
    origin_id = get_station_id(origin_name)
    dest_id = get_station_id(destination_name)

    if not origin_id or not dest_id:
        print("Could not resolve station names.")
        return None

    params = {
        "from": origin_id,
        "to": dest_id,
        "results": 6,
        "departure": time if time != "now" else None
    }

    response = requests.get(f"{API_BASE}/journeys", params=params)
    if response.ok:
        data = response.json()
        with open("journeys.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Journey data saved to journeys.json")
        return data
    else:
        print("Failed to fetch journey data")
        return None

if __name__ == "__main__":
    from_input = input("Enter origin station name: ")
    to_input = input("Enter destination station name: ")
    time_input = input("Enter time (HH:MM or 'now'): ")

    fetch_journeys(from_input, to_input, time_input)