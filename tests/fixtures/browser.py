import os
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page

from tests.fixtures.config import (
    DEFAULT_NAVIGATION_TIMEOUT,
    DEFAULT_TIMEOUT,
    SERVICES,
    VIDEO_DIR,
    VIEWPORT_HEIGHT,
    VIEWPORT_WIDTH,
)


class PageHelper:
    def __init__(self, page: Page):
        self.page = page

    def goto_fast(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def goto_and_wait(self, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.page.goto(url, timeout=timeout)
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_text(self, text: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(f"text={text}", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_and_wait(self, selector: str, timeout: int = 5000) -> None:
        self.page.click(selector, timeout=timeout)
        self.page.wait_for_load_state("domcontentloaded")

    def fill_and_submit(self, selector: str, value: str, submit_selector: str | None = None) -> None:
        self.page.fill(selector, value)
        if submit_selector:
            self.page.click(submit_selector)

    def take_screenshot(self, name: str) -> str:
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / f"{name}.png"
        self.page.screenshot(path=str(path))
        return str(path)

    def is_visible(self, selector: str) -> bool:
        try:
            return self.page.is_visible(selector)
        except Exception:
            return False

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector) or ""

    def get_value(self, selector: str) -> str:
        return self.page.input_value(selector)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "args": [
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        "ignore_https_errors": True,
        "record_video_dir": str(VIDEO_DIR) if os.getenv("RECORD_VIDEO") else None,
        "record_har_path": "test-results/har/" if os.getenv("RECORD_HAR") else None,
    }


@pytest.fixture(scope="session")
def asset_lens_url() -> str:
    return SERVICES["asset_lens"]["url"]


@pytest.fixture(scope="session")
def ts_demo_url() -> str:
    return SERVICES["ts_demo"]["url"]


@pytest.fixture(scope="session")
def solo_chat_url() -> str:
    return SERVICES["solo_chat"]["url"]


@pytest.fixture(scope="session")
def stock_analyzer_url() -> str:
    return SERVICES["stock_analyzer"]["url"]


@pytest.fixture(scope="session")
def lobster_url() -> str:
    return SERVICES["lobster"]["url"]


@pytest.fixture
def page_helper(page: Page) -> PageHelper:
    return PageHelper(page)


@pytest.fixture(scope="module")
def shared_context(browser_type_launch_args: dict, browser_type: type) -> Generator[BrowserContext, None, None]:
    browser = browser_type.launch(**browser_type_launch_args)
    context = browser.new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        ignore_https_errors=True,
    )
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="module")
def shared_page(shared_context: BrowserContext) -> Generator[Page, None, None]:
    page = shared_context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
    yield page
    page.close()
