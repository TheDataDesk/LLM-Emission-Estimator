import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def build_prompt(journeys):
    prompt = "You are a sustainability assistant. Summarize the CO₂ impact of these public transport journeys in Berlin.\n\n"

    for idx, j in enumerate(journeys, 1):
        prompt += f"Route {idx} (CO₂: {j['co2']:.0f}g)\n"
        for leg in j['legs']:
            prompt += f"{leg.strip()}\n"
        prompt += "\n"

    prompt += (
        "Compare the routes. Mention which modes emit CO₂ and why, "
        "highlight the fully electric modes (U-Bahn, Tram), "
        "and recommend the most sustainable option with reasoning.\n"
        "End with a positive fact about Berlin's transit or climate efforts."
    )
    return prompt

def query_ollama_summary(journeys):
    prompt = build_prompt(journeys)
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        return f" Failed to generate summary: {response.status_code} - {response.text}"