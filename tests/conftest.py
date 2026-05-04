"""
E2E Tests Configuration.
E2E 测试配置

功能:
1. 多项目测试支持 (asset-lens, solo-chat, stock-analyzer)
2. 失败时自动截图和录像
3. 服务健康检查
4. 测试辅助工具
5. 并行测试支持
"""

import os
import time
from pathlib import Path
from typing import Generator

import pytest
import requests
from playwright.sync_api import Page, BrowserContext, Browser, Playwright


PROJECT_ROOT = Path(__file__).parent.parent.parent
SCREENSHOT_DIR = Path("test-results/screenshots")
VIDEO_DIR = Path("test-results/videos")
TRACE_DIR = Path("test-results/traces")

# 服务配置
SERVICES = {
    "asset_lens": {
        "url": os.getenv("ASSET_LENS_URL", "http://localhost:8000"),
        "health_endpoint": "/",
    },
    "solo_chat": {
        "url": os.getenv("SOLO_CHAT_URL", "http://localhost:5173"),
        "health_endpoint": "/",
    },
    "stock_analyzer": {
        "url": os.getenv("STOCK_ANALYZER_URL", "http://localhost:8001"),
        "health_endpoint": "/",
    },
    "lobster": {
        "url": os.getenv("LOBSTER_URL", "http://localhost:8002"),
        "health_endpoint": "/",
    },
}


def check_server_health(base_url: str, health_endpoint: str = "/", timeout: int = 3) -> bool:
    """检查服务器是否运行"""
    try:
        response = requests.get(f"{base_url}{health_endpoint}", timeout=timeout)
        return response.status_code in [200, 404, 307]
    except Exception:
        return False


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """浏览器启动配置"""
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
    """浏览器上下文配置"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "record_video_dir": str(VIDEO_DIR) if os.getenv("RECORD_VIDEO") else None,
        "record_har_path": "test-results/har/" if os.getenv("RECORD_HAR") else None,
    }


@pytest.fixture(scope="session")
def asset_lens_url() -> str:
    """asset-lens 服务 URL"""
    return SERVICES["asset_lens"]["url"]


@pytest.fixture(scope="session")
def solo_chat_url() -> str:
    """solo-chat 服务 URL"""
    return SERVICES["solo_chat"]["url"]


@pytest.fixture(scope="session")
def stock_analyzer_url() -> str:
    """stock-analyzer 服务 URL"""
    return SERVICES["stock_analyzer"]["url"]


@pytest.fixture(scope="session")
def lobster_url() -> str:
    """lobster 服务 URL"""
    return SERVICES["lobster"]["url"]


@pytest.fixture(scope="session", autouse=True)
def setup_directories() -> Generator[None, None, None]:
    """创建测试结果目录"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    yield


@pytest.fixture(autouse=True)
def setup_page(page: Page, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """页面设置"""
    page.set_default_timeout(15000)
    page.set_default_navigation_timeout(30000)

    yield page

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        _save_failure_artifacts(page, request)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """测试结果钩子 - 用于失败截图"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _save_failure_artifacts(page: Page, request: pytest.FixtureRequest) -> None:
    """保存失败时的截图和 HTML"""
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


class APITester:
    """API 测试辅助类"""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def get(self, endpoint: str, expected_status: list | None = None) -> dict:
        """发送 GET 请求并验证响应"""
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.get(url)

        if expected_status:
            assert response.status in expected_status, f"期望状态码 {expected_status}，实际 {response.status}"

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}

    def post(self, endpoint: str, data: dict | None = None, expected_status: list | None = None) -> dict:
        """发送 POST 请求并验证响应"""
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.post(url, data=data)

        if expected_status:
            assert response.status in expected_status, f"期望状态码 {expected_status}，实际 {response.status}"

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}

    def delete(self, endpoint: str, expected_status: list | None = None) -> dict:
        """发送 DELETE 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.delete(url)

        if expected_status:
            assert response.status in expected_status

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}


@pytest.fixture
def api_tester(page: Page, request: pytest.FixtureRequest) -> APITester:
    """API 测试辅助工具"""
    # 根据测试标记选择服务 URL
    if "asset_lens" in request.node.keywords:
        base_url = SERVICES["asset_lens"]["url"]
    elif "solo_chat" in request.node.keywords:
        base_url = SERVICES["solo_chat"]["url"]
    elif "stock_analyzer" in request.node.keywords:
        base_url = SERVICES["stock_analyzer"]["url"]
    elif "lobster" in request.node.keywords:
        base_url = SERVICES["lobster"]["url"]
    else:
        base_url = SERVICES["asset_lens"]["url"]

    return APITester(page, base_url)


class PageHelper:
    """页面操作辅助类"""

    def __init__(self, page: Page):
        self.page = page

    def goto_fast(self, url: str) -> None:
        """快速导航 - 只等待 DOM 加载"""
        self.page.goto(url, wait_until="domcontentloaded")

    def goto_and_wait(self, url: str, timeout: int = 15000) -> None:
        """导航到页面并等待加载完成"""
        self.page.goto(url, timeout=timeout)
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_text(self, text: str, timeout: int = 5000) -> None:
        """等待文本出现"""
        self.page.wait_for_selector(f"text={text}", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        """等待选择器出现"""
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_and_wait(self, selector: str, timeout: int = 5000) -> None:
        """点击元素并等待响应"""
        self.page.click(selector, timeout=timeout)
        self.page.wait_for_load_state("domcontentloaded")

    def fill_and_submit(self, selector: str, value: str, submit_selector: str | None = None) -> None:
        """填充表单并提交"""
        self.page.fill(selector, value)
        if submit_selector:
            self.page.click(submit_selector)

    def take_screenshot(self, name: str) -> str:
        """截图"""
        screenshot_dir = Path("test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / f"{name}.png"
        self.page.screenshot(path=str(path))
        return str(path)

    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        try:
            return self.page.is_visible(selector)
        except Exception:
            return False

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.text_content(selector) or ""

    def get_value(self, selector: str) -> str:
        """获取输入框值"""
        return self.page.input_value(selector)


@pytest.fixture
def page_helper(page: Page) -> PageHelper:
    """页面操作辅助工具"""
    return PageHelper(page)


@pytest.fixture(scope="module")
def shared_context(browser_type_launch_args: dict, browser_type: type) -> Generator[BrowserContext, None, None]:
    """共享浏览器上下文"""
    browser = browser_type.launch(**browser_type_launch_args)
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="module")
def shared_page(shared_context: BrowserContext) -> Generator[Page, None, None]:
    """共享页面"""
    page = shared_context.new_page()
    page.set_default_timeout(15000)
    page.set_default_navigation_timeout(30000)
    yield page
    page.close()
