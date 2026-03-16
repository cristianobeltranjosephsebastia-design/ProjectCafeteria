import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key_env = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key_env)

for m in client.models.list():
    print(f"Modelo Disponible: {m.name}")