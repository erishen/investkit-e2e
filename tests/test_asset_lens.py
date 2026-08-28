import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper, SharedTestHelpers


@pytest.mark.asset_lens
@pytest.mark.ui
class TestAssetLensUI:
    def test_homepage_loads(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_homepage_loads(page, page_helper, asset_lens_url, ["Asset", "Lens", "投资", "资产"])

    def test_navigation_menu(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            asset_lens_url,
            ["nav", "header", "[role='navigation']", ".navbar"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestAssetLensAPI:
    def test_health_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_health_endpoint(api_tester)

    def test_api_docs(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_docs(api_tester)

    def test_openapi_json(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/openapi.json",
            expected_keys=["openapi", "paths"],
        )

    def test_portfolio_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/portfolio/summary")

    def test_stocks_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/stocks")

    def test_market_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/market/overview")

    def test_risk_endpoint(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(api_tester, "/api/risk/metrics")


@pytest.mark.asset_lens
@pytest.mark.slow
class TestAssetLensPerformance:
    def test_page_load_time(self, page: Page, asset_lens_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_load_time(page_helper, asset_lens_url)

    def test_api_response_time(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_response_time(api_tester)
