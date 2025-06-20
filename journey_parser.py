import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  

def build_prompt(user_input):
    return f"""You are a helpful assistant that extracts travel information from user input.

Your task is to extract the origin, destination, and time from the user's message.

Respond ONLY in this JSON format:
{{
  "origin": "...",
  "destination": "...",
  "time": "..."
}}

Example input: "I want to go from Alexanderplatz to Grunewald at 5pm"
Expected response:
{{
  "origin": "Alexanderplatz",
  "destination": "Grunewald",
  "time": "17:00"
}}

User input: "{user_input}"
"""


def parse_input_with_llm(user_input):
    payload = {
        "model": MODEL,
        "prompt": build_prompt(user_input),
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.ok:
            raw = response.json()["response"]
            match = re.search(r"{.*}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            else:
                print("No JSON found in LLM response")
        else:
            print("Failed to contact Ollama:", response.status_code)
    except Exception as e:
        print("LLM Parse Error:", e)

    return None

if __name__ == "__main__":
    query = input("Where would you like to go? ")
    result = parse_input_with_llm(query)
    if result:
        print("Parsed:", result)
    else:
        print("Could not parse your input.")