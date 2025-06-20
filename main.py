from journey_parser import parse_input_with_llm
from api_fetcher import fetch_journeys
from carbon_calculator import summarize_journeys
from summary import query_ollama_summary
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    print("Welcome to the LLM-powered Carbon Route Assistant!")
    print("Type your route query (e.g., 'I want to go from Alexanderplatz to Grunewald at 17:00')\n")

    while True:
        user_input = input("Where do you want to go? (or type 'exit' to quit):\n> ")

        if user_input.lower().strip() == "exit":
            print("Goodbye!")
            break

        parsed = parse_input_with_llm(user_input)
        if not parsed:
            print("Could not parse your input. Try again.")
            continue

        print(f"Searching routes: {parsed['origin']} → {parsed['destination']} at {parsed['time']}...")

        result = fetch_journeys(parsed["origin"], parsed["destination"], parsed["time"])
        if not result:
            print(" No journeys found or API failed.")
            continue

        time.sleep(1)
        summaries = summarize_journeys("journeys.json")

        if not summaries:
            print("No journeys to display.")
            continue

        print("\nROUTE OPTIONS:")
        for idx, route in enumerate(summaries, 1):
            print(f"\n--- Route {idx} ---")
            for leg in route["legs"]:
                print(leg)
            print(f"Departure: {route['departure']} | Total CO₂: {route['co2']:.0f}g")

        print("\n AI Summary:")
        ai_summary = query_ollama_summary(summaries)
        print(ai_summary)
        print("\n")

if __name__ == "__main__":
    main()