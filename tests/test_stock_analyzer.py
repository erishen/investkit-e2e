import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper, SharedTestHelpers


@pytest.mark.stock_analyzer
@pytest.mark.ui
class TestStockAnalyzerUI:
    def test_homepage_loads(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_homepage_loads(
            page, page_helper, stock_analyzer_url, ["Stock", "Analyzer", "股票", "分析"]
        )

    def test_dashboard_exists(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            stock_analyzer_url,
            [".dashboard", "[data-testid='dashboard']", ".main-content", "#app"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestStockAnalyzerAPI:
    def test_health_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_health_endpoint(api_tester)

    def test_api_docs(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_docs(api_tester)

    def test_signals_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/signals")

    def test_stocks_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/stocks")

    def test_backtest_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/backtest")

    def test_score_endpoint(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/score")


@pytest.mark.stock_analyzer
@pytest.mark.slow
class TestStockAnalyzerPerformance:
    def test_page_load_time(self, page: Page, stock_analyzer_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_load_time(page_helper, stock_analyzer_url)

    def test_api_response_time(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_response_time(api_tester)
