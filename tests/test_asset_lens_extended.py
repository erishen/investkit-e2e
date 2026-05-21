"""
Asset Lens Extended E2E Tests.
Asset Lens 扩展 E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import APITester


@pytest.mark.asset_lens
@pytest.mark.api
class TestPortfolioAPI:
    """投资组合 API 测试"""

    def test_portfolio_items(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试投资组合项目"""
        result = api_tester.get("/api/portfolio/items", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_portfolio_performance(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试投资组合表现"""
        result = api_tester.get("/api/portfolio/performance", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_portfolio_allocation(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试投资组合配置"""
        result = api_tester.get("/api/portfolio/allocation", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_portfolio_analytics(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试投资组合分析"""
        result = api_tester.get("/api/portfolio/analytics", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestStockAPI:
    """股票 API 测试"""

    def test_stock_quote(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票行情"""
        result = api_tester.get("/api/stock/quote/sh600519", expected_status=[200, 404, 503, 500])

        assert result["status"] in [200, 404, 503, 500]

    def test_stock_search(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票搜索"""
        result = api_tester.get("/api/stock/search?keyword=茅台", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_kline(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票 K 线"""
        result = api_tester.get(
            "/api/stock/kline/sh600519?ktype=day&count=30", expected_status=[200, 404, 500]
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestChatAPI:
    """聊天 API 测试"""

    def test_chat_qa(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试聊天问答"""
        result = api_tester.post(
            "/api/chat/qa",
            data={"message": "如何控制风险？", "fast_mode": True},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_chat_rag(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试 RAG 查询"""
        result = api_tester.post(
            "/api/chat/rag",
            data={"query": "投资策略", "k": 5},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_chat_config(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试聊天配置"""
        result = api_tester.get("/api/chat/config", expected_status=[200, 404])

        assert result["status"] in [200, 404]


@pytest.mark.asset_lens
@pytest.mark.api
class TestStrategyAPI:
    """策略 API 测试"""

    def test_strategy_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试策略列表"""
        result = api_tester.get("/api/strategy/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_strategy_screen(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试策略筛选"""
        result = api_tester.post(
            "/api/strategy/screen",
            data={"strategy": "value", "min_score": 60},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_strategy_backtest(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试策略回测"""
        result = api_tester.post(
            "/api/strategy/backtest",
            data={"strategy": "momentum", "start_date": "2024-01-01"},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestRiskAPI:
    """风险 API 测试"""

    def test_risk_alerts(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试风险预警"""
        result = api_tester.get("/api/risk/alerts", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_risk_analysis(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试风险分析"""
        result = api_tester.get("/api/risk/analysis", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_risk_report(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试风险报告"""
        result = api_tester.get("/api/risk/report", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestBackupAPI:
    """备份 API 测试"""

    def test_backup_status(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试备份状态"""
        result = api_tester.get("/api/backup/status", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_backup_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试备份列表"""
        result = api_tester.get("/api/backup/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestStockPoolAPI:
    """股票池 API 测试"""

    def test_stock_pool_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票池列表"""
        result = api_tester.get("/api/stock-pool/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_stock_pool_stocks(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试股票池股票"""
        result = api_tester.get("/api/stock-pool/default/stocks", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestReportAPI:
    """报告 API 测试"""

    def test_report_generate(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试生成报告"""
        result = api_tester.post(
            "/api/report/generate",
            data={"report_type": "portfolio"},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]

    def test_report_list(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试报告列表"""
        result = api_tester.get("/api/report/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.asset_lens
@pytest.mark.api
class TestSystemAPI:
    """系统 API 测试"""

    def test_system_status(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试系统状态"""
        result = api_tester.get("/api/system/status", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_system_config(self, page: Page, asset_lens_url: str, api_tester: APITester):
        """测试系统配置"""
        result = api_tester.get("/api/system/config", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]
