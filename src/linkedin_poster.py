"""LinkedIn post publisher for Aipply."""

import logging
import time

logger = logging.getLogger(__name__)


class LinkedInPoster:
    """Publishes posts to a LinkedIn profile using Playwright."""

    def __init__(self, scanner):
        self.scanner = scanner
        self.page = scanner._page

    def publish_post(self, content: str) -> bool:
        """Publish a text post to LinkedIn."""

        if not content or not content.strip():
            raise ValueError("Post content is empty.")

        content = content.strip()

        logger.info("Opening LinkedIn homepage...")

        self.page.goto(
            "https://www.linkedin.com/feed/",
            wait_until="domcontentloaded",
        )

        self.page.wait_for_timeout(3000)

        logger.info("Current URL: %s", self.page.url)

        # Check whether LinkedIn redirected us to authentication.
        if "/login" in self.page.url or "/authwall" in self.page.url:
            raise RuntimeError(
                "LinkedIn is not logged in. Please log in to LinkedIn "
                "in the browser profile first."
            )

        # Find the "Start a post" button.
        start_post = self.page.get_by_text("Start a post", exact=True)

        if start_post.count() == 0:
            raise RuntimeError(
                "Could not find the 'Start a post' button."
            )

        logger.info("Clicking 'Start a post'...")

        start_post.first.click()

        self.page.wait_for_timeout(2000)

        # Find the post editor.
        editor = self.page.locator(
            '[contenteditable="true"]'
        )

        if editor.count() == 0:
            raise RuntimeError(
                "Could not find the LinkedIn post editor."
            )

        logger.info("Entering post content...")

        editor.last.fill(content)

        self.page.wait_for_timeout(1000)

        # Find the Post button inside the dialog.
        post_button = self.page.get_by_role(
            "button",
            name="Post",
            exact=True,
        )

        if post_button.count() == 0:
            raise RuntimeError(
                "Could not find the final 'Post' button."
            )

        logger.info("Publishing post...")

        post_button.last.click()

        # Give LinkedIn time to publish.
        self.page.wait_for_timeout(4000)

        logger.info("Post published successfully.")

        return True