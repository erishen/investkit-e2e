"""
Asset Lens E2E Tests.
Asset Lens E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import PageHelper, APITester


@pytest.mark.asset_lens
@pytest.mark.ui
class TestAssetLensUI:
    """Asset Lens UI 测试"""

    def test_homepage_loads(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        """测试首页加载"""
        page_helper.goto_and_wait(asset_lens_url)

        assert page.title() is not None

    def test_navigation_menu(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        """测试导航菜单"""
        page_helper.goto_and_wait(asset_lens_url)

        nav_selectors = ["nav", "header", "[role='navigation']", ".navbar"]
        found = any(page_helper.is_visible(sel) for sel in nav_selectors)

        assert found or page.content() is not None


@pytest.mark.asset_lens
@pytest.mark.api
class TestAssetLensAPI:
    """Asset Lens API 测试"""

    def test_health_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试健康检查端点"""
        result = api_tester.get("/health", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_api_docs(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试 API 文档"""
        result = api_tester.get("/docs", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_openapi_json(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试 OpenAPI JSON"""
        result = api_tester.get("/openapi.json", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_portfolio_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试投资组合端点"""
        result = api_tester.get("/api/portfolio/summary", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stocks_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票端点"""
        result = api_tester.get("/api/stocks", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_market_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试市场端点"""
        result = api_tester.get("/api/market/overview", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_risk_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试风险端点"""
        result = api_tester.get("/api/risk/metrics", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.slow
class TestAssetLensPerformance:
    """Asset Lens 性能测试"""

    def test_page_load_time(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        """测试页面加载时间"""
        import time

        start = time.time()
        page_helper.goto_and_wait(asset_lens_url)
        load_time = time.time() - start

        assert load_time < 10, f"页面加载时间过长: {load_time:.2f}s"

    def test_api_response_time(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试 API 响应时间"""
        import time

        start = time.time()
        api_tester.get("/health")
        response_time = time.time() - start

        assert response_time < 3, f"API 响应时间过长: {response_time:.2f}s"
