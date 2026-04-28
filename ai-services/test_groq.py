import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": "Explain AI in one sentence"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.json())