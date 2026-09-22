from src.linkedin_scanner import LinkedInScanner
from src.gemini_client import GeminiClient
from src.utils import load_config


# ---------------------------------------------------------
# Load configuration
# ---------------------------------------------------------
settings = load_config("config/settings.yaml")
profile = load_config("config/profile.yaml")

candidate = profile["candidate"]


# ---------------------------------------------------------
# Initialize scanner and Gemini
# ---------------------------------------------------------
scanner = LinkedInScanner(settings)
gemini = GeminiClient(config=settings)


try:
    # -----------------------------------------------------
    # Get real LinkedIn job
    # -----------------------------------------------------
    scanner.connect_browser()

    job_url = "https://www.linkedin.com/jobs/view/4460322289/"

    print("\nGetting job details...")
    job = scanner.get_job_details(job_url)

    print("\n===== JOB =====")
    print("Title:", job["title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Job ID:", job["linkedin_job_id"])


    # -----------------------------------------------------
    # Generate tailored material with Gemini
    # -----------------------------------------------------
    print("\nGenerating application material with Gemini...")

    result = gemini.generate_job_materials(
        job_description=job["description"],
        candidate_profile=candidate,
        company=job["company"],
        role=job["title"],
    )


    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------
    print("\n" + "=" * 60)
    print("GEMINI GENERATED SUMMARY")
    print("=" * 60)

    print(result["summary"])


    print("\n" + "=" * 60)
    print("GEMINI GENERATED COMPETENCIES")
    print("=" * 60)

    for i, skill in enumerate(result["competencies"], start=1):
        print(f"{i}. {skill}")


    print("\n" + "=" * 60)
    print("GEMINI GENERATED COVER LETTER")
    print("=" * 60)

    print(result["cover_letter"])


finally:
    scanner.close()