from src.linkedin_scanner import LinkedInScanner
from src.utils import load_config

settings = load_config("config/settings.yaml")

scanner = LinkedInScanner(settings)

try:
    scanner.connect_browser()

    jobs = scanner.search_jobs(
        keywords="Machine Learning Engineer",
        location="Pakistan",
        max_results=1,
    )

    print("\n===== JOBS FOUND =====")

    for job in jobs:
        print("\nTitle:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("URL:", job["url"])
        print("Job ID:", job["linkedin_job_id"])

finally:
    scanner.close()