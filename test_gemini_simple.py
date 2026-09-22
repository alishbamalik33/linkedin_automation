import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not loaded.")

print("API key loaded.")
print("Creating Gemini client...")

client = genai.Client(api_key=api_key)

print("Sending test request...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Reply with exactly: Gemini is working.",
)

print("Response received.")
print(response.text)