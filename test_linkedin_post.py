from pathlib import Path
from datetime import datetime
import json

import yaml

from src.linkedin_scanner import LinkedInScanner
from src.linkedin_poster import LinkedInPoster
from src.utils import load_config


POSTS_FILE = Path("linkedin_content/posts.yaml")
POSTED_FILE = Path("linkedin_content/posted.json")


def load_posts():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("posts", [])


def load_posted():
    if not POSTED_FILE.exists():
        return {"posted": []}

    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posted(data):
    with open(POSTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_next_post(posts, posted_data):
    posted_ids = {
        item["id"]
        for item in posted_data.get("posted", [])
    }

    for post in posts:
        if post["id"] not in posted_ids:
            return post

    return None


settings = load_config("config/settings.yaml")

posts = load_posts()
posted_data = load_posted()

post = get_next_post(posts, posted_data)

if post is None:
    print("All posts have already been published.")
    exit()

print("=" * 60)
print("NEXT LINKEDIN POST")
print("=" * 60)

print("Post ID:", post["id"])
print("Scheduled date:", post["date"])

print("\nContent:")
print(post["content"])

print("\nConnecting to LinkedIn...")

scanner = LinkedInScanner(settings)

try:
    scanner.connect_browser()

    poster = LinkedInPoster(scanner)

    print("\nPublishing post...")

    success = poster.publish_post(post["content"])

    if success:
        posted_data["posted"].append(
            {
                "id": post["id"],
                "posted_at": datetime.now().isoformat(),
            }
        )

        save_posted(posted_data)

        print("\n" + "=" * 60)
        print("POST PUBLISHED AND RECORDED")
        print("=" * 60)

finally:
    scanner.close()