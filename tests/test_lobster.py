import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, SharedTestHelpers


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterHealthAPI:
    def test_health_endpoint(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_health_endpoint(api_tester)

    def test_api_docs(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_docs(api_tester)


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterInvestAPI:
    def test_signals_endpoint(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/invest/signals",
            expected_keys=["signals", "data", "items", "results"],
        )

    def test_portfolio_endpoint(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/invest/portfolio",
            expected_keys=["portfolio", "data", "items", "holdings"],
        )

    def test_risk_endpoint(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/invest/risk",
            expected_keys=["risk", "data", "items", "metrics"],
        )

    def test_market_endpoint(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/invest/market",
            expected_keys=["market", "data", "items", "indices"],
        )


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterRAGAPI:
    def test_rag_status(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/rag/status",
            expected_keys=["status", "data", "ready", "enabled"],
        )

    def test_rag_query(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/rag/query",
            expected_keys=["answer", "data", "results", "documents"],
            method="post", data={"query": "投资策略", "k": 5},
        )


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterSchedulerAPI:
    def test_scheduler_list(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/scheduler/list",
            expected_keys=["tasks", "data", "items", "jobs"],
        )

    def test_scheduler_status(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/scheduler/status",
            expected_keys=["status", "data", "running", "enabled"],
        )


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterMemoryAPI:
    def test_memory_list(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/memory/list",
            expected_keys=["memories", "data", "items", "records"],
        )

    def test_memory_search(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/memory/search",
            expected_keys=["results", "data", "items", "memories"],
            method="post", data={"query": "测试", "limit": 10},
        )


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterLLMAPI:
    def test_llm_status(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/llm/status",
            expected_keys=["status", "data", "model", "ready"],
        )

    def test_llm_chat(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/llm/chat",
            expected_keys=["response", "data", "message", "content"],
            method="post", data={"message": "你好", "stream": False},
        )


@pytest.mark.lobster
@pytest.mark.api
class TestLobsterDataAPI:
    def test_data_status(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/data/status",
            expected_keys=["status", "data", "sources", "last_sync"],
        )

    def test_data_sync(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester, "/api/data/sync",
            expected_keys=["status", "data", "sync_id", "result"],
            method="post", data={"source": "sina"},
        )


@pytest.mark.lobster
@pytest.mark.slow
class TestLobsterPerformance:
    def test_api_response_time(self, page: Page, api_tester: APITester):
        SharedTestHelpers.assert_api_response_time(api_tester)
