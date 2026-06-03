import time
from collections.abc import Generator

import pytest
from playwright.sync_api import Page

from tests.fixtures.api import APITester, SharedTestHelpers, api_tester
from tests.fixtures.browser import (
    PageHelper,
    asset_lens_url,
    browser_context_args,
    browser_type_launch_args,
    lobster_url,
    page_helper,
    shared_context,
    shared_page,
    solo_chat_url,
    stock_analyzer_url,
    ts_demo_url,
)
from tests.fixtures.config import (
    DEFAULT_NAVIGATION_TIMEOUT,
    DEFAULT_TIMEOUT,
    SCREENSHOT_DIR,
    TRACE_DIR,
    VIDEO_DIR,
)


@pytest.fixture(scope="session", autouse=True)
def setup_directories() -> Generator[None, None, None]:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    yield


@pytest.fixture(autouse=True)
def setup_page(page: Page, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT)
    yield page
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        _save_failure_artifacts(page, request)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _save_failure_artifacts(page: Page, request: pytest.FixtureRequest) -> None:
    test_name = request.node.name.replace("[", "_").replace("]", "_")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
    html_path = SCREENSHOT_DIR / f"{test_name}_{timestamp}.html"
    try:
        page.screenshot(path=str(screenshot_path))
        print(f"\n📸 截图已保存: {screenshot_path}")
    except Exception as e:
        print(f"\n⚠️ 截图失败: {e}")
    try:
        html_content = page.content()
        html_path.write_text(html_content, encoding="utf-8")
        print(f"📄 HTML 已保存: {html_path}")
    except Exception as e:
        print(f"⚠️ HTML 保存失败: {e}")
