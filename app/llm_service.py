from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("API key found:", api_key is not None)

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL = "gpt-oss-120b:free"


def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that returns clean structured JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM API call failed.")
        print("Reason:", e)
        return None