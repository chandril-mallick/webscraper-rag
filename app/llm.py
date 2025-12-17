import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"   # ✅ correct name

def generate_answer(context: str, query: str) -> str:
    prompt = f"""
You are a helpful AI assistant.
Answer ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]
