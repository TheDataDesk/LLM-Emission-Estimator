# Carbon Route Assistant (Terminal Version)

A local AI-powered assistant that lets you enter **natural language queries** like:

> "I want to go from Alexanderplatz to Grunewald at 17:00"

It then:
- Parses your query using a local **LLaMA3 model** via Ollama
- Fetches real-time public transport journeys from the **VBB API**
- Calculates **CO₂ emissions** per journey using segment distances and transport mode
- Generates a natural language **summary and recommendation**
- All inside your **terminal**, without sending data to the cloud

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running
- A CPU-capable LLM (like `llama3`) pulled via Ollama

---

## Setup


1. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Pull the model with Ollama**

```bash
ollama pull llama3
```

4. **Run Ollama in background**

```bash
ollama run llama3
```

5. **Run the main**

```bash
python main.py
```

---