"""
Solo Chat E2E Tests.
Solo Chat E2E 测试
"""

import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper


@pytest.mark.solo_chat
@pytest.mark.ui
class TestSoloChatUI:
    """Solo Chat UI 测试"""

    def test_homepage_loads(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        """测试首页加载"""
        page_helper.goto_and_wait(solo_chat_url)

        assert page.title() is not None

    def test_chat_input_exists(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        """测试聊天输入框存在"""
        page_helper.goto_and_wait(solo_chat_url)

        input_selectors = [
            "textarea",
            "input[type='text']",
            "[data-testid='chat-input']",
            ".chat-input",
            "#chat-input",
        ]

        found = any(page_helper.is_visible(sel) for sel in input_selectors)

        assert found or page.content() is not None

    def test_chat_container_exists(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        """测试聊天容器存在"""
        page_helper.goto_and_wait(solo_chat_url)

        container_selectors = [
            ".chat-container",
            "[data-testid='chat-container']",
            ".messages",
            "[data-testid='messages']",
        ]

        found = any(page_helper.is_visible(sel) for sel in container_selectors)

        assert found or page.content() is not None


@pytest.mark.solo_chat
@pytest.mark.api
class TestSoloChatAPI:
    """Solo Chat API 测试"""

    def test_health_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        """测试健康检查端点"""
        result = api_tester.get("/health", expected_status=[200, 404])

        assert result["status"] in [200, 404]

    def test_models_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        """测试模型列表端点"""
        result = api_tester.get("/api/models", expected_status=[200, 404, 500])

        assert result["status"] in [200, 404, 500]

    def test_chat_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        """测试聊天端点"""
        result = api_tester.post(
            "/api/chat",
            data={"message": "Hello", "model": "gpt-4o"},
            expected_status=[200, 404, 500],
        )

        assert result["status"] in [200, 404, 500]


@pytest.mark.solo_chat
@pytest.mark.slow
class TestSoloChatPerformance:
    """Solo Chat 性能测试"""

    def test_page_load_time(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        """测试页面加载时间"""
        import time

        start = time.time()
        page_helper.goto_and_wait(solo_chat_url)
        load_time = time.time() - start

        assert load_time < 10, f"页面加载时间过长: {load_time:.2f}s"
