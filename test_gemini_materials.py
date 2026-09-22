import json

from src.gemini_client import GeminiClient
from src.utils import load_config


# ---------------------------------------------------------
# Load configuration
# ---------------------------------------------------------
settings = load_config("config/settings.yaml")
profile = load_config("config/profile.yaml")

candidate = profile["candidate"]


# ---------------------------------------------------------
# Create Gemini client
# ---------------------------------------------------------
print("Creating Gemini client...")

gemini = GeminiClient(config=settings)

print("Gemini client created.")


# ---------------------------------------------------------
# Small test job
# ---------------------------------------------------------
job_description = """
We are looking for an AI Engineer.

Requirements:
- Python
- Machine learning
- Generative AI
- RAG
- Experience with LLM applications
- Strong communication skills

The candidate will work on AI-powered applications and retrieval
augmented generation systems.
"""

print("Calling generate_job_materials()...")


# ---------------------------------------------------------
# Generate materials
# ---------------------------------------------------------
result = gemini.generate_job_materials(
    job_description=job_description,
    candidate_profile=candidate,
    company="Test Company",
    role="AI Engineer",
)


# ---------------------------------------------------------
# Display result
# ---------------------------------------------------------
print("\n" + "=" * 60)
print("GENERATED RESULT")
print("=" * 60)

print(json.dumps(result, indent=2, ensure_ascii=False))