import pytest
from playwright.sync_api import Page

from tests.conftest import APITester, PageHelper, SharedTestHelpers


@pytest.mark.solo_chat
@pytest.mark.ui
class TestSoloChatUI:
    def test_homepage_loads(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_homepage_loads(page, page_helper, solo_chat_url, ["Chat", "Solo", "聊天", "对话"])

    def test_chat_input_exists(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            solo_chat_url,
            ["textarea", "input[type='text']", "[data-testid='chat-input']", ".chat-input", "#chat-input"],
        )

    def test_chat_container_exists(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_content_visible(
            page,
            page_helper,
            solo_chat_url,
            [".chat-container", "[data-testid='chat-container']", ".messages", "[data-testid='messages']"],
        )


@pytest.mark.solo_chat
@pytest.mark.api
class TestSoloChatAPI:
    def test_health_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        SharedTestHelpers.assert_health_endpoint(api_tester)

    def test_models_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/models",
            expected_keys=["models", "data", "items", "list"],
        )

    def test_chat_endpoint(self, page: Page, solo_chat_url: str, api_tester: APITester):
        SharedTestHelpers.assert_api_endpoint(
            api_tester,
            "/api/chat",
            expected_keys=["response", "data", "message", "content"],
            method="post",
            data={"message": "Hello", "model": "gpt-4o"},
        )


@pytest.mark.solo_chat
@pytest.mark.slow
class TestSoloChatPerformance:
    def test_page_load_time(self, page: Page, solo_chat_url: str, page_helper: PageHelper):
        SharedTestHelpers.assert_page_load_time(page_helper, solo_chat_url)
