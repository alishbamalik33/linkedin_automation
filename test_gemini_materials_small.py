import json
from src.gemini_client import GeminiClient
from src.utils import load_config

settings = load_config("config/settings.yaml")
profile = load_config("config/profile.yaml")
candidate = profile["candidate"]

gemini = GeminiClient(config=settings)

small_job_description = """
AI Engineer

Requirements:
- Python
- Machine Learning
- Generative AI
- RAG
"""

print("Calling generate_job_materials() with small prompt...")

result = gemini.generate_job_materials(
    job_description=small_job_description,
    candidate_profile=candidate,
    company="Test Company",
    role="AI Engineer",
)

print("\n===== RESULT =====")
print(json.dumps(result, indent=2, ensure_ascii=False))