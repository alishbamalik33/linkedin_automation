from src.linkedin_scanner import LinkedInScanner
from src.utils import load_config

settings = load_config("config/settings.yaml")

scanner = LinkedInScanner(settings)

try:
    scanner.connect_browser()

    job_url = "https://www.linkedin.com/jobs/view/4460322289/"

    job = scanner.get_job_details(job_url)

    print("\n===== JOB DETAILS =====")
    print("Title:", job["title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Job ID:", job["linkedin_job_id"])

    print("\n===== JOB DESCRIPTION =====")
    print(job["description"])

    print("\n===== DESCRIPTION LENGTH =====")
    print(len(job["description"]), "characters")

finally:
    scanner.close()