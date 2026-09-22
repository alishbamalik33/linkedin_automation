# from src.gemini_client import GeminiClient
# from src.utils import load_config

# settings = load_config("config/settings.yaml")

# gemini = GeminiClient(config=settings)

# candidate_profile = {
#     "name": "Alishba Ishrat",
#     "education": "BS Mathematics, International Islamic University Islamabad, CGPA 3.53",
#     "skills": [
#         "Python",
#         "Machine Learning",
#         "Deep Learning",
#         "TensorFlow",
#         "PyTorch",
#         "Computer Vision",
#         "OpenCV",
#         "FastAPI",
#         "Generative AI",
#         "RAG",
#         "LangChain",
#         "ChromaDB",
#         "Docker"
#     ],
#     "experience": [
#         "AI/ML internship and project experience",
#         "Machine learning and computer vision projects",
#         "AI application development using Python"
#     ],
#     "projects": [
#         "Content-Based Movie Recommendation System",
#         "YOLO-based staff dress classification",
#         "ATM card detection",
#         "Emotion recognition",
#         "RAG-based applications"
#     ]
# }

# job_description = """
# We are looking for an entry-level AI/ML Engineer to work on
# machine learning and generative AI applications.

# Requirements:
# - Strong Python programming skills
# - Understanding of machine learning and deep learning
# - Experience with TensorFlow or PyTorch
# - Knowledge of computer vision
# - Familiarity with Generative AI and RAG
# - Ability to build and integrate AI applications
# """

# result = gemini.generate_job_materials(
#     job_description=job_description,
#     candidate_profile=candidate_profile,
#     company="Example AI Company",
#     role="AI/ML Engineer"
# )

# print("\n===== SUMMARY =====")
# print(result["summary"])

# print("\n===== COMPETENCIES =====")
# for skill in result["competencies"]:
#     print("-", skill)

# print("\n===== COVER LETTER =====")
# print(result["cover_letter"])

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Reply with exactly: Gemini is working."
)

print(response.text)