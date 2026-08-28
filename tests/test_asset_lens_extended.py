import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, SharedTestHelpers


@pytest.mark.asset_lens
@pytest.mark.api
class TestPortfolioAPI:
    def test_portfolio_items(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/portfolio/items",
            expected_keys=["items", "data", "portfolio", "stocks"],
        )

    def test_portfolio_performance(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/portfolio/performance",
            expected_keys=["performance", "data", "returns", "metrics"],
        )

    def test_portfolio_allocation(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/portfolio/allocation",
            expected_keys=["allocation", "data", "sectors", "weights"],
        )

    def test_portfolio_analytics(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/portfolio/analytics",
            expected_keys=["analytics", "data", "metrics", "sharpe"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestStockAPI:
    def test_stock_quote(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stock/quote/sh600519",
            expected_keys=["price", "data", "quote", "close"],
        )

    def test_stock_search(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stock/search?keyword=茅台",
            expected_keys=["results", "data", "stocks", "items"],
        )

    def test_stock_kline(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stock/kline/sh600519?ktype=day&count=30",
            expected_keys=["kline", "data", "candles", "ohlc"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestChatAPI:
    def test_chat_qa(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/chat/qa",
            expected_keys=["answer", "data", "response", "content"],
            method="post",
            data={"message": "如何控制风险？", "fast_mode": True},
        )

    def test_chat_rag(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/chat/rag",
            expected_keys=["answer", "data", "results", "documents"],
            method="post",
            data={"query": "投资策略", "k": 5},
        )

    def test_chat_config(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/chat/config",
            expected_keys=["config", "data", "model", "settings"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestStrategyAPI:
    def test_strategy_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/strategy/list",
            expected_keys=["strategies", "data", "items", "list"],
        )

    def test_strategy_screen(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/strategy/screen",
            expected_keys=["results", "data", "stocks", "items"],
            method="post",
            data={"strategy": "value", "min_score": 60},
        )

    def test_strategy_backtest(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/strategy/backtest",
            expected_keys=["total_return", "results", "data", "status"],
            method="post",
            data={"strategy": "momentum", "start_date": "2024-01-01"},
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestRiskAPI:
    def test_risk_alerts(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/risk/alerts",
            expected_keys=["alerts", "data", "items", "warnings"],
        )

    def test_risk_analysis(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/risk/analysis",
            expected_keys=["analysis", "data", "metrics", "var"],
        )

    def test_risk_report(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/risk/report",
            expected_keys=["report", "data", "summary", "metrics"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestBackupAPI:
    def test_backup_status(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/backup/status",
            expected_keys=["status", "data", "last_backup", "enabled"],
        )

    def test_backup_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/backup/list",
            expected_keys=["backups", "data", "items", "list"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestStockPoolAPI:
    def test_stock_pool_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stock-pool/list",
            expected_keys=["pools", "data", "items", "list"],
        )

    def test_stock_pool_stocks(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stock-pool/default/stocks",
            expected_keys=["stocks", "data", "items", "list"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestReportAPI:
    def test_report_generate(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/report/generate",
            expected_keys=["report", "data", "status", "url"],
            method="post",
            data={"report_type": "portfolio"},
        )

    def test_report_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/report/list",
            expected_keys=["reports", "data", "items", "list"],
        )


@pytest.mark.asset_lens
@pytest.mark.api
class TestSystemAPI:
    def test_system_status(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/system/status",
            expected_keys=["status", "data", "uptime", "version"],
        )

    def test_system_config(self, page: Page, asset_lens_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/system/config",
            expected_keys=["config", "data", "settings", "app"],
        )
