import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_response(prompt, retries=3):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    for attempt in range(retries):
        try:
            response = requests.post(URL, headers=headers, json=data, timeout=10)

            if response.status_code != 200:
                raise Exception(response.text)

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    return "AI service unavailable"