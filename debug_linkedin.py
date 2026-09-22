from src.linkedin_scanner import LinkedInScanner
from src.utils import load_config

settings = load_config("config/settings.yaml")

scanner = LinkedInScanner(settings)

try:
    page = scanner.connect_browser()

    url = "https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer&location=Pakistan"

    print("Opening LinkedIn...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)

    page.wait_for_timeout(3000)

    print("\n========================================")
    print("If LinkedIn asks you to sign in,")
    print("please sign in normally in the browser.")
    print("After you are logged in and can see the")
    print("job listings, return to this terminal.")
    print("========================================\n")

    input("Press ENTER after LinkedIn is logged in...")

    print("\n===== PAGE INFORMATION =====")
    print("URL:", page.url)
    print("TITLE:", page.title())

    print("\n===== JOB LINKS =====")

    job_links = page.query_selector_all("a[href*='/jobs/view/']")
    print("Links containing /jobs/view/:", len(job_links))

    for i, link in enumerate(job_links[:10], 1):
        print(f"\n--- Job link {i} ---")
        print("Text:", link.inner_text().strip())
        print("Href:", link.get_attribute("href"))

    print("\n===== ALL LINKS =====")

    all_links = page.query_selector_all("a")
    print("Total <a> elements:", len(all_links))

    for i, link in enumerate(all_links[:30], 1):
        text = link.inner_text().strip()
        href = link.get_attribute("href")

        if text or href:
            print(f"{i}. TEXT={text[:100]!r} | HREF={href!r}")

    print("\n===== JOB-RELATED HTML =====")

    html = page.content()

    for keyword in [
        "AI Engineer",
        "Machine Learning Engineer",
        "jobs/view",
        "Soliton",
    ]:
        print(
            f"{keyword!r}:",
            keyword.lower() in html.lower()
        )

finally:
    scanner.close()