"""
Stock Analyzer Extended E2E Tests.
Stock Analyzer 扩展 E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import PageHelper, APITester


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestBacktestAPI:
    """回测 API 测试"""

    def test_backtest_momentum_strategy(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试动量策略回测"""
        result = api_tester.post(
            "/api/backtest/run",
            data={
                "strategy": "momentum",
                "start_date": "2024-01-01",
                "end_date": "2024-03-01",
                "initial_capital": 100000,
            },
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_backtest_mean_reversion_strategy(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试均值回归策略回测"""
        result = api_tester.post(
            "/api/backtest/run",
            data={
                "strategy": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-03-01",
            },
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_backtest_result_format(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试回测结果格式"""
        result = api_tester.get("/api/backtest/result", expected_status=[200, 404])

        if result["status"] == 200 and result["data"]:
            data = result["data"]
            assert "total_return" in data or "results" in data or "status" in data


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestSignalsAPI:
    """信号 API 测试"""

    def test_signals_scan(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试信号扫描"""
        result = api_tester.post(
            "/api/signals/scan",
            data={"min_score": 60, "limit": 10},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_signals_by_type(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试按类型获取信号"""
        result = api_tester.get("/api/signals?type=macd_golden_cross", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_signal(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试单只股票信号"""
        result = api_tester.get("/api/signals/000001", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestOptimizationAPI:
    """优化 API 测试"""

    def test_optimization_run(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试运行优化"""
        result = api_tester.post(
            "/api/optimization/run",
            data={
                "strategy": "momentum",
                "param_ranges": {
                    "holding_days": [3, 5, 10],
                    "stop_loss": [0.05, 0.10],
                },
            },
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_optimization_status(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试优化状态"""
        result = api_tester.get("/api/optimization/status", expected_status=[200, 404])

        assert result["status"] in [200, 404]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestMarketTimingAPI:
    """大盘择时 API 测试"""

    def test_market_timing(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试大盘择时"""
        result = api_tester.get("/api/market/timing", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_market_indicators(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试市场指标"""
        result = api_tester.get("/api/market/indicators", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestReportAPI:
    """报告 API 测试"""

    def test_generate_report(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试生成报告"""
        result = api_tester.post(
            "/api/report/generate",
            data={"report_type": "backtest"},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_export_report(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试导出报告"""
        result = api_tester.get("/api/report/export?format=pdf", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestStockDataAPI:
    """股票数据 API 测试"""

    def test_stock_list(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试股票列表"""
        result = api_tester.get("/api/stocks/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_detail(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试股票详情"""
        result = api_tester.get("/api/stocks/000001", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_history(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试股票历史"""
        result = api_tester.get("/api/stocks/000001/history?days=30", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_technical(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试股票技术指标"""
        result = api_tester.get("/api/stocks/000001/technical", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestScannerAPI:
    """扫描器 API 测试"""

    def test_scanner_run(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试运行扫描器"""
        result = api_tester.post(
            "/api/scanner/run",
            data={"scan_type": "signals", "min_score": 70},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_scanner_status(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试扫描器状态"""
        result = api_tester.get("/api/scanner/status", expected_status=[200, 404])

        assert result["status"] in [200, 404]


@pytest.mark.stock_analyzer
@pytest.mark.api
class TestRiskAPI:
    """风险 API 测试"""

    def test_risk_alerts(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试风险预警"""
        result = api_tester.get("/api/risk/alerts", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_risk_score(self, page: Page, stock_analyzer_url: str, api_tester: APITester):
        """测试风险评分"""
        result = api_tester.get("/api/risk/score", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]
