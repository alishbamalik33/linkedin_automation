from src.linkedin_scanner import LinkedInScanner
from src.utils import load_config

settings = load_config("config/settings.yaml")

scanner = LinkedInScanner(settings)

try:
    scanner.connect_browser()

    job_url = "https://www.linkedin.com/jobs/view/4460322289/"

    page = scanner._page

    page.goto(
        job_url,
        wait_until="domcontentloaded",
        timeout=30_000,
    )

    page.wait_for_timeout(3000)

    print("\n===== PAGE TITLE =====")
    print(page.title())

    print("\n===== H1 ELEMENTS =====")
    h1s = page.query_selector_all("h1")

    for i, h1 in enumerate(h1s):
        try:
            print(f"\nH1 #{i + 1}")
            print("TEXT:", repr(h1.inner_text()))
            print("HTML:")
            print(h1.evaluate("(el) => el.outerHTML"))
        except Exception as exc:
            print("Error:", exc)

    print("\n===== COMPANY LINKS =====")
    company_links = page.query_selector_all("a[href*='/company/']")

    for i, link in enumerate(company_links[:10]):
        try:
            print(f"\nCompany link #{i + 1}")
            print("TEXT:", repr(link.inner_text()))
            print("HTML:")
            print(link.evaluate("(el) => el.outerHTML"))
        except Exception as exc:
            print("Error:", exc)

    print("\n===== TOP PAGE HTML =====")

    # Print a limited amount of HTML so the terminal does not become huge.
    html = page.locator("body").inner_html()

    print(html[:15000])

finally:
    scanner.close()