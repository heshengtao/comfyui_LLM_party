"""
Unit tests for API Route Loader integration.
"""

import importlib.util
import os
import sys
from unittest import mock
import pytest

# Load api_route_loader.py directly from file path
_loader_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "custom_tool",
    "api_route_loader.py",
)
_spec = importlib.util.spec_from_file_location("api_route_loader", _loader_path)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["api_route_loader"] = _mod
_spec.loader.exec_module(_mod)

api_route_Chat = _mod.api_route_Chat
api_route_loader = _mod.api_route_loader
_format_api_route_error = _mod._format_api_route_error
NODE_CLASS_MAPPINGS = _mod.NODE_CLASS_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = _mod.NODE_DISPLAY_NAME_MAPPINGS


class TestApiRouteLoader:
    def test_node_mappings(self):
        assert "api_route_loader" in NODE_CLASS_MAPPINGS
        assert NODE_CLASS_MAPPINGS["api_route_loader"] is api_route_loader
        assert "api_route_loader" in NODE_DISPLAY_NAME_MAPPINGS
        assert "API Route" in NODE_DISPLAY_NAME_MAPPINGS["api_route_loader"]

    def test_input_types(self):
        inputs = api_route_loader.INPUT_TYPES()
        assert "required" in inputs
        assert "model_name" in inputs["required"]
        assert "optional" in inputs
        assert "api_key" in inputs["optional"]
        assert "base_url" in inputs["optional"]
        assert "custom_model" in inputs["optional"]
        assert inputs["optional"]["base_url"][1]["default"] == "https://global.api-route.com/v1"

    def test_chatbot_instantiation(self):
        loader = api_route_loader()
        (chat,) = loader.chatbot("claude-sonnet-4-5", api_key="sk-test", base_url="https://global.api-route.com/v1")
        assert isinstance(chat, api_route_Chat)
        assert chat.model_name == "claude-sonnet-4-5"
        assert chat.api_key == "sk-test"
        assert chat.base_url == "https://global.api-route.com/v1"

    def test_chatbot_custom_model(self):
        loader = api_route_loader()
        (chat,) = loader.chatbot("claude-sonnet-4-5", api_key="sk-test", custom_model="custom-model-x")
        assert chat.model_name == "custom-model-x"

    def test_error_formatting(self):
        ex = type("AuthenticationError", (Exception,), {"__module__": "openai"})("Invalid key")
        err = _format_api_route_error(ex)
        assert "[API Route Auth Error]" in err

    def test_chat_send_mock(self):
        chat = api_route_Chat("claude-sonnet-4-5", api_key="sk-test")
        mock_client = mock.MagicMock()
        mock_choice = mock.MagicMock()
        mock_choice.message.content = "Hello from API Route"
        mock_choice.message.reasoning_content = None
        mock_resp = mock.MagicMock()
        mock_resp.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_resp

        with mock.patch("api_route_loader.OpenAI", return_value=mock_client):
            history = []
            content, hist, reasoning = chat.send("Hi", 0.7, 100, history)
            assert content == "Hello from API Route"
            assert len(hist) == 2
            assert hist[0]["role"] == "user"
            assert hist[1]["role"] == "assistant"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
