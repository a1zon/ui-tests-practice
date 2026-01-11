from playwright.sync_api import Page


class NavigationHelper:

    @staticmethod
    def safe_goto(page: Page, url: str, retries: int = 3) -> None:
        for attempt in range(1, retries + 1):
            try:
                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )
                return
            except Exception:
                if attempt == retries:
                    raise
