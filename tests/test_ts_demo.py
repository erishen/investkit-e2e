import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper, SharedTestHelpers


@pytest.mark.ts_demo
@pytest.mark.ui
class TestTSDemoUI:
    def test_homepage_loads(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_homepage_loads(page, page_helper, ts_demo_url, ["Demo", "TS", "投资", "分析"])

    def test_navigation_menu(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            ts_demo_url,
            ["nav", "header", "[role='navigation']", ".navbar", "nav nav"],
        )

    def test_dashboard_visible(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            ts_demo_url,
            [".dashboard", "[data-testid='dashboard']", ".main-content", "#app", ".portfolio"],
        )


@pytest.mark.ts_demo
@pytest.mark.api
class TestTSDemoAPI:
    def test_health_endpoint(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_health_endpoint(api_tester)

    def test_api_portfolio(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/portfolio",
            expected_keys=["portfolio", "data", "items", "holdings"],
        )

    def test_api_calculate(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/calculate",
            expected_keys=["result", "data", "value", "returns"],
        )

    def test_api_analyze(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/analyze",
            expected_keys=["analysis", "data", "results", "metrics"],
        )

    def test_api_compare(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/compare",
            expected_keys=["comparison", "data", "results", "items"],
        )

    def test_api_report(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/report",
            expected_keys=["report", "data", "summary", "url"],
        )


@pytest.mark.ts_demo
@pytest.mark.api
class TestTSDemoDataAPI:
    def test_data_products(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/data/products",
            expected_keys=["products", "data", "items", "list"],
        )

    def test_data_exchange_rates(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/data/exchange-rates",
            expected_keys=["rates", "data", "items", "exchange_rates"],
        )

    def test_data_north_flow(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/data/north-flow",
            expected_keys=["flow", "data", "items", "north_flow"],
        )


@pytest.mark.ts_demo
@pytest.mark.slow
class TestTSDemoPerformance:
    def test_page_load_time(self, page: Page, ts_demo_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_load_time(page_helper, ts_demo_url)

    def test_api_response_time(self, page: Page, ts_demo_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_response_time(api_tester)
