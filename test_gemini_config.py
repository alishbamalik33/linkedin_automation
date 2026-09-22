from src.gemini_client import GeminiClient
from src.utils import load_config

settings = load_config("config/settings.yaml")

print("Creating Gemini client...")
gemini = GeminiClient(config=settings)

print("Calling generate_text()...")

result = gemini.generate_text(
    "Reply with exactly: Aipply Gemini test successful."
)

print("\nRESULT:")
print(result)