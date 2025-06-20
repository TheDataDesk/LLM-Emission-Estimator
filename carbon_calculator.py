import json
from geopy.distance import geodesic

# Emission factors in kg per person per km
EMISSION_FACTORS = {
    'bus': 0.096,
    'tram': 0.0,
    'subway': 0.0,
    'train': 0.041,
    'suburban': 0.041,
    'ferry': 0.17,
    'walk': 0.0,
    'bicycle': 0.0
}

MODE_MAP = {
    "bus": "🚌 Bus",
    "tram": "🚋 Tram",
    "subway": "🚇 U-Bahn",
    "train": "🚉 S-Bahn",
    "suburban": "🚉 S-Bahn",
    "ferry": "⛴ Ferry",
    "walk": "🚶 Walk",
    "bicycle": "🚴 Bicycle"
}

def calculate_distance_km(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

def estimate_emission(distance_km, mode):
    factor = EMISSION_FACTORS.get(mode.lower(), 0.06)
    return round(distance_km * factor * 1000, 2)  # grams

def summarize_journeys(file_path="journeys.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    journeys = data.get("journeys", [])
    summaries = []

    for j in journeys:
        try:
            legs = j["legs"]
            dep_time = legs[0]["departure"]
            arr_time = legs[-1]["arrival"]
        except:
            continue

        total_co2 = 0
        leg_summaries = []

        for leg in legs:
            mode = (
                leg.get("mode") or
                leg.get("line", {}).get("product") or
                leg.get("line", {}).get("mode") or
                "unknown"
            )
            if mode == "unknown":
                continue

            orig = leg["origin"]["location"]
            dest = leg["destination"]["location"]
            dist = calculate_distance_km(orig["latitude"], orig["longitude"],
                                         dest["latitude"], dest["longitude"])

            co2 = estimate_emission(dist, mode)
            total_co2 += co2

            line = leg.get("line", {}).get("name", "")
            dirn = leg.get("direction", "")
            operator = leg.get("line", {}).get("operator", {}).get("name", "")
            orig_name = leg["origin"]["name"]
            dest_name = leg["destination"]["name"]

            summary = f"{MODE_MAP.get(mode, mode.title())} {line} → {dirn}"
            summary += f"From: {orig_name} → To: {dest_name}"
            summary += f"Operator: {operator} | Distance: {dist:.2f} km | CO₂: {co2:.0f}g"

            leg_summaries.append(summary)

        journey_summary = {
            "departure": dep_time,
            "legs": leg_summaries,
            "co2": total_co2
        }
        summaries.append(journey_summary)

    return summaries