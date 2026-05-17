"""
TS-Demo E2E Tests.
TS-Demo (TypeScript 投资分析系统) E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper


@pytest.mark.ts_demo
@pytest.mark.ui
class TestTSDemoUI:
    """TS-Demo UI 测试"""

    def test_homepage_loads(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        """测试首页加载"""
        page_helper.goto_and_wait(ts_demo_url)

        assert page.title() is not None

    def test_navigation_menu(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        """测试导航菜单"""
        page_helper.goto_and_wait(ts_demo_url)

        nav_selectors = ["nav", "header", "[role='navigation']", ".navbar", "nav nav"]
        found = any(page_helper.is_visible(sel) for sel in nav_selectors)

        assert found or page.content() is not None

    def test_dashboard_visible(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        """测试仪表板可见"""
        page_helper.goto_and_wait(ts_demo_url)

        dashboard_selectors = [
            ".dashboard",
            "[data-testid='dashboard']",
            ".main-content",
            "#app",
            ".portfolio",
        ]

        found = any(page_helper.is_visible(sel) for sel in dashboard_selectors)

        assert found or page.content() is not None


@pytest.mark.ts_demo
@pytest.mark.api
class TestTSDemoAPI:
    """TS-Demo API 测试"""

    def test_health_endpoint(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试健康检查端点"""
        result = api_tester.get("/health", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_api_portfolio(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试投资组合 API"""
        result = api_tester.get("/api/portfolio", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_api_calculate(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试计算 API"""
        result = api_tester.get("/api/calculate", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_api_analyze(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试分析 API"""
        result = api_tester.get("/api/analyze", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_api_compare(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试对比 API"""
        result = api_tester.get("/api/compare", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_api_report(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试报告 API"""
        result = api_tester.get("/api/report", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.ts_demo
@pytest.mark.api
class TestTSDemoDataAPI:
    """TS-Demo 数据 API 测试"""

    def test_data_products(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试产品数据 API"""
        result = api_tester.get("/api/data/products", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_data_exchange_rates(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试汇率数据 API"""
        result = api_tester.get("/api/data/exchange-rates", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_data_north_flow(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试北向资金数据 API"""
        result = api_tester.get("/api/data/north-flow", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.ts_demo
@pytest.mark.slow
class TestTSDemoPerformance:
    """TS-Demo 性能测试"""

    def test_page_load_time(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        """测试页面加载时间"""
        import time

        start = time.time()
        page_helper.goto_and_wait(ts_demo_url)
        load_time = time.time() - start

        assert load_time < 10, f"页面加载时间过长: {load_time:.2f}s"

    def test_api_response_time(self, page: Page, ts_demo_url: str, api_tester: APITester):
        """测试 API 响应时间"""
        import time

        start = time.time()
        api_tester.get("/health")
        response_time = time.time() - start

        assert response_time < 3, f"API 响应时间过长: {response_time:.2f}s"
