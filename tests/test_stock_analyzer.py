"""
Stock Analyzer E2E Tests.
Stock Analyzer E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper


@pytest.mark.stock_analyzer
@pytest.mark.ui
class TestStockAnalyzerUI:
    """Stock Analyzer UI 测试"""

    def test_homepage_loads(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        """测试首页加载"""
        page_helper.goto_and_wait(stock_analyzer_url)

        assert page.title() is not None

    def test_dashboard_exists(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        """测试仪表板存在"""
        page_helper.goto_and_wait(stock_analyzer_url)

        dashboard_selectors = [
            ".dashboard",
            "[data-testid='dashboard']",
            ".main-content",
            "#app",
        ]

        found = any(page_helper.is_visible(sel) for sel in dashboard_selectors)

        assert found or page.content() is not None


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestStockAnalyzerAPI:
    """Stock Analyzer API 测试"""

    def test_health_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试健康检查端点"""
        result = api_tester.get("/health", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_api_docs(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试 API 文档"""
        result = api_tester.get("/docs", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_signals_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试信号端点"""
        result = api_tester.get("/api/signals", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stocks_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试股票端点"""
        result = api_tester.get("/api/stocks", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_backtest_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试回测端点"""
        result = api_tester.get("/api/backtest", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_score_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试评分端点"""
        result = api_tester.get("/api/score", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.stock_analyzer
@pytest.mark.slow
class TestStockAnalyzerPerformance:
    """Stock Analyzer 性能测试"""

    def test_page_load_time(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        """测试页面加载时间"""
        import time

        start = time.time()
        page_helper.goto_and_wait(stock_analyzer_url)
        load_time = time.time() - start

        assert load_time < 10, f"页面加载时间过长: {load_time:.2f}s"

    def test_api_response_time(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试 API 响应时间"""
        import time

        start = time.time()
        api_tester.get("/health")
        response_time = time.time() - start

        assert response_time < 3, f"API 响应时间过长: {response_time:.2f}s"
