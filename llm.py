import requests

def generate_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 80,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "stop": ["User:", "\nUser:", "Conversation Memory:"]
                }
            }
        )

        result = response.json()
        return result.get("response", "").strip()

    except Exception as e:
        return f"Error connecting to Ollama: {e}"
