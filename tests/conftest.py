import importlib.util
import re
import time
import urllib.error
import urllib.request
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
    SERVICES,
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


def _service_up(url: str, timeout: float = 2.0) -> bool:
    """Probe a service base URL; any HTTP response (even 4xx/5xx) counts as up."""
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except urllib.error.HTTPError:
        return True
    except OSError:
        return False


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    """Skip service-bound E2E tests when the target service is unreachable,
    and investkit-utils tests when the package is not installed (e.g. CI)."""
    for item in items:
        mod_name = item.module.__name__
        if mod_name == "tests.test_investkit_utils":
            if importlib.util.find_spec("investkit_utils") is None:
                item.add_marker(pytest.mark.skip(reason="investkit_utils is not installed"))
            continue
        # tests.test_<service>[_extended] -> SERVICES key
        m = re.fullmatch(r"tests\.test_([a-z_]+?)(_extended)?", mod_name)
        if not m:
            continue
        service = SERVICES.get(m.group(1))
        if service and not _service_up(service["url"]):
            item.add_marker(pytest.mark.skip(reason=f"{m.group(1)} service unreachable at {service['url']}"))


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
