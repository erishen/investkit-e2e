import time

import pytest
from playwright.sync_api import Page

from tests.fixtures.config import (
    ERROR_STATUS_THRESHOLD,
    MAX_API_RESPONSE_SECONDS,
    MAX_PAGE_LOAD_SECONDS,
    MIN_PAGE_CONTENT_LENGTH,
    SERVICES,
)


class APITester:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def get(self, endpoint: str, expected_status: list | None = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.get(url)

        if expected_status:
            assert response.status in expected_status, (
                f"期望状态码 {expected_status}，实际 {response.status}"
            )
        else:
            assert response.status < 500, (
                f"服务器错误，状态码 {response.status}，端点 {endpoint}"
            )

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}

    def post(
        self, endpoint: str, data: dict | None = None, expected_status: list | None = None
    ) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.post(url, data=data)

        if expected_status:
            assert response.status in expected_status, (
                f"期望状态码 {expected_status}，实际 {response.status}"
            )
        else:
            assert response.status < 500, (
                f"服务器错误，状态码 {response.status}，端点 {endpoint}"
            )

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}

    def delete(self, endpoint: str, expected_status: list | None = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = self.page.request.delete(url)

        if expected_status:
            assert response.status in expected_status, (
                f"期望状态码 {expected_status}，实际 {response.status}"
            )
        else:
            assert response.status < 500, (
                f"服务器错误，状态码 {response.status}，端点 {endpoint}"
            )

        try:
            return {"status": response.status, "data": response.json()}
        except Exception:
            return {"status": response.status, "data": None}


class SharedTestHelpers:
    @staticmethod
    def assert_homepage_loads(page, page_helper, base_url, expected_keywords):
        page_helper.goto_and_wait(base_url)
        title = page.title()
        assert title != "", "页面标题为空"
        assert any(kw in title for kw in expected_keywords), (
            f"页面标题应包含项目关键词，实际标题: {title}"
        )

    @staticmethod
    def assert_health_endpoint(api_tester):
        result = api_tester.get("/health", expected_status=[200, 404])
        if result["status"] == 200 and result["data"]:
            assert "status" in result["data"] or "health" in str(result["data"]).lower(), (
                "健康检查响应应包含 status 字段或 health 信息"
            )

    @staticmethod
    def assert_api_docs(api_tester):
        result = api_tester.get("/docs", expected_status=[200, 404])
        if result["status"] == 200 and result["data"]:
            assert "openapi" in str(result["data"]).lower() or "paths" in str(result["data"]).lower(), (
                "API 文档响应应包含 openapi 或 paths 信息"
            )

    @staticmethod
    def assert_page_load_time(page_helper, base_url, max_seconds=MAX_PAGE_LOAD_SECONDS):
        start = time.time()
        page_helper.goto_and_wait(base_url)
        load_time = time.time() - start
        assert load_time < max_seconds, f"页面加载时间过长: {load_time:.2f}s"

    @staticmethod
    def assert_api_response_time(api_tester, max_seconds=MAX_API_RESPONSE_SECONDS):
        start = time.time()
        api_tester.get("/health")
        response_time = time.time() - start
        assert response_time < max_seconds, f"API 响应时间过长: {response_time:.2f}s"

    @staticmethod
    def assert_api_endpoint(api_tester, endpoint, expected_keys=None, method="get", data=None):
        if method == "post":
            result = api_tester.post(endpoint, data=data, expected_status=[200, 404])
        else:
            result = api_tester.get(endpoint, expected_status=[200, 404])

        if result["status"] == 200 and result["data"]:
            assert isinstance(result["data"], (dict, list)), f"{endpoint} 响应应为 dict 或 list"
            if isinstance(result["data"], dict) and expected_keys:
                assert any(k in result["data"] for k in expected_keys), (
                    f"{endpoint} 响应应包含 {expected_keys} 字段"
                )

    @staticmethod
    def assert_page_content_visible(page, page_helper, base_url, selectors):
        page_helper.goto_and_wait(base_url)
        content = page.content()
        assert len(content) > MIN_PAGE_CONTENT_LENGTH, (
            f"页面内容过短，可能未正确加载，长度: {len(content)}"
        )
        found = any(page_helper.is_visible(sel) for sel in selectors)
        assert found, f"未找到预期内容，页面标题: {page.title()}"


@pytest.fixture
def api_tester(page: Page, request: pytest.FixtureRequest) -> APITester:
    if "asset_lens" in request.node.keywords:
        base_url = SERVICES["asset_lens"]["url"]
    elif "ts_demo" in request.node.keywords:
        base_url = SERVICES["ts_demo"]["url"]
    elif "solo_chat" in request.node.keywords:
        base_url = SERVICES["solo_chat"]["url"]
    elif "stock_analyzer" in request.node.keywords:
        base_url = SERVICES["stock_analyzer"]["url"]
    elif "lobster" in request.node.keywords:
        base_url = SERVICES["lobster"]["url"]
    else:
        base_url = SERVICES["asset_lens"]["url"]

    return APITester(page, base_url)
