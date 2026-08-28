import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, SharedTestHelpers


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestBacktestAPI:
    def test_backtest_momentum_strategy(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/backtest/run",
            expected_keys=["total_return", "results", "status", "data"],
            method="post",
            data={
                "strategy": "momentum",
                "start_date": "2024-01-01",
                "end_date": "2024-03-01",
                "initial_capital": 100000,
            },
        )

    def test_backtest_mean_reversion_strategy(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/backtest/run",
            expected_keys=["total_return", "results", "status", "data"],
            method="post",
            data={"strategy": "mean_reversion", "start_date": "2024-01-01", "end_date": "2024-03-01"},
        )

    def test_backtest_result_format(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/backtest/result",
            expected_keys=["total_return", "results", "status"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestSignalsAPI:
    def test_signals_scan(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/signals/scan",
            expected_keys=["signals", "data", "items", "results"],
            method="post",
            data={"min_score": 60, "limit": 10},
        )

    def test_signals_by_type(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/signals?type=macd_golden_cross",
            expected_keys=["signals", "data", "items", "type"],
        )

    def test_stock_signal(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/signals/000001",
            expected_keys=["signal", "data", "signals", "score"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestOptimizationAPI:
    def test_optimization_run(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/optimization/run",
            expected_keys=["results", "data", "status", "best_params"],
            method="post",
            data={"strategy": "momentum", "param_ranges": {"holding_days": [3, 5, 10], "stop_loss": [0.05, 0.10]}},
        )

    def test_optimization_status(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/optimization/status",
            expected_keys=["status", "data", "progress", "running"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestMarketTimingAPI:
    def test_market_timing(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/market/timing",
            expected_keys=["timing", "data", "signal", "indicator"],
        )

    def test_market_indicators(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/market/indicators",
            expected_keys=["indicators", "data", "pe", "pb"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestReportAPI:
    def test_generate_report(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/report/generate",
            expected_keys=["report", "data", "status", "url"],
            method="post",
            data={"report_type": "backtest"},
        )

    def test_export_report(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/report/export?format=pdf",
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestStockDataAPI:
    def test_stock_list(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stocks/list",
            expected_keys=["stocks", "data", "items", "list"],
        )

    def test_stock_detail(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stocks/000001",
            expected_keys=["stock", "data", "name", "code"],
        )

    def test_stock_history(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stocks/000001/history?days=30",
            expected_keys=["history", "data", "candles", "prices"],
        )

    def test_stock_technical(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/stocks/000001/technical",
            expected_keys=["technical", "data", "macd", "rsi"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestScannerAPI:
    def test_scanner_run(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/scanner/run",
            expected_keys=["results", "data", "items", "status"],
            method="post",
            data={"scan_type": "signals", "min_score": 70},
        )

    def test_scanner_status(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/scanner/status",
            expected_keys=["status", "data", "running", "progress"],
        )


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestRiskAPI:
    def test_risk_alerts(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/risk/alerts",
            expected_keys=["alerts", "data", "items", "warnings"],
        )

    def test_risk_score(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/risk/score",
            expected_keys=["score", "data", "risk", "level"],
        )
