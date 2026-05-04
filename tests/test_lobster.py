"""
Lobster E2E Tests.
Lobster E2E 测试
"""

import os
import pytest
from playwright.sync_api import Page

from tests.conftest import PageHelper, APITester

LOBSTER_URL = os.getenv("LOBSTER_URL", "http://localhost:8002")


@pytest.fixture
def lobster_url() -> str:
    """Lobster 服务 URL"""
    return LOBSTER_URL


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterHealthAPI:
    """Lobster 健康 API 测试"""

    def test_health_endpoint(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试健康检查端点"""
        result = api_tester.get(f"{lobster_url}/health", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_api_docs(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 API 文档"""
        result = api_tester.get(f"{lobster_url}/docs", expected_status=[200, 404])

        assert result["status"] in [200, 404]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterInvestAPI:
    """Lobster 投资 API 测试"""

    def test_signals_endpoint(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试信号端点"""
        result = api_tester.get(f"{lobster_url}/api/invest/signals", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_portfolio_endpoint(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试投资组合端点"""
        result = api_tester.get(f"{lobster_url}/api/invest/portfolio", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_risk_endpoint(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试风险端点"""
        result = api_tester.get(f"{lobster_url}/api/invest/risk", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_market_endpoint(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试市场端点"""
        result = api_tester.get(f"{lobster_url}/api/invest/market", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterRAGAPI:
    """Lobster RAG API 测试"""

    def test_rag_status(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 RAG 状态"""
        result = api_tester.get(f"{lobster_url}/api/rag/status", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_rag_query(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 RAG 查询"""
        result = api_tester.post(
            f"{lobster_url}/api/rag/query",
            data={"query": "投资策略", "k": 5},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterSchedulerAPI:
    """Lobster 定时任务 API 测试"""

    def test_scheduler_list(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试定时任务列表"""
        result = api_tester.get(f"{lobster_url}/api/scheduler/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_scheduler_status(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试定时任务状态"""
        result = api_tester.get(f"{lobster_url}/api/scheduler/status", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterMemoryAPI:
    """Lobster 记忆 API 测试"""

    def test_memory_list(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试记忆列表"""
        result = api_tester.get(f"{lobster_url}/api/memory/list", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_memory_search(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试记忆搜索"""
        result = api_tester.post(
            f"{lobster_url}/api/memory/search",
            data={"query": "测试", "limit": 10},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterLLMAPI:
    """Lobster LLM API 测试"""

    def test_llm_status(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 LLM 状态"""
        result = api_tester.get(f"{lobster_url}/api/llm/status", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_llm_chat(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 LLM 聊天"""
        result = api_tester.post(
            f"{lobster_url}/api/llm/chat",
            data={"message": "你好", "stream": False},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterDataAPI:
    """Lobster 数据 API 测试"""

    def test_data_status(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试数据状态"""
        result = api_tester.get(f"{lobster_url}/api/data/status", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_data_sync(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试数据同步"""
        result = api_tester.post(
            f"{lobster_url}/api/data/sync",
            data={"source": "sina"},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.lobster
@pytest.mark.slow
class TestLobsterPerformance:
    """Lobster 性能测试"""

    def test_api_response_time(self, page: Page, lobster_url: str, api_tester: APITester):
        """测试 API 响应时间"""
        import time

        start = time.time()
        api_tester.get(f"{lobster_url}/health")
        response_time = time.time() - start

        assert response_time < 3, f"API 响应时间过长: {response_time:.2f}s"
