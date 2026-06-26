"""
Comprehensive tests for LiteLLM Loader integration.

Run unit tests (no API key needed):
    python -m pytest test/test_litellm_loader.py -v -k "not live"

Run live E2E tests (requires API key in env):
    python -m pytest test/test_litellm_loader.py -v -k "live"
"""

import importlib.util
import os
import sys
import types
from types import SimpleNamespace
from unittest import mock

import pytest

# Load litellm_loader.py directly from file path without triggering parent package __init__
_loader_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "custom_tool", "litellm_loader.py")
_spec = importlib.util.spec_from_file_location("litellm_loader", _loader_path)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["litellm_loader"] = _mod
_spec.loader.exec_module(_mod)

litellm_Chat = _mod.litellm_Chat
litellm_loader = _mod.litellm_loader
_format_litellm_error = _mod._format_litellm_error
NODE_CLASS_MAPPINGS = _mod.NODE_CLASS_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = _mod.NODE_DISPLAY_NAME_MAPPINGS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_message(content="Hello", reasoning_content=None, tool_calls=None):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    if reasoning_content is not None:
        msg.reasoning_content = reasoning_content
    return msg


def _make_response(content="Hello", reasoning_content=None, tool_calls=None):
    msg = _make_message(content=content, reasoning_content=reasoning_content, tool_calls=tool_calls)
    choice = SimpleNamespace(message=msg)
    return SimpleNamespace(choices=[choice])


def _make_stream_chunks(text_chunks):
    chunks = []
    for text in text_chunks:
        delta = SimpleNamespace(content=text, tool_calls=None)
        choice = SimpleNamespace(delta=delta)
        chunks.append(SimpleNamespace(choices=[choice]))
    return chunks


def _fresh_history(system_prompt="You are a helpful assistant."):
    return [{"role": "system", "content": system_prompt}]


# ===========================================================================
# UNIT TESTS
# ===========================================================================


class TestLiteLLMChatInit:
    def test_basic_init(self):
        chat = litellm_Chat("openai/gpt-4o-mini")
        assert chat.model_name == "openai/gpt-4o-mini"
        assert chat.api_key == ""
        assert chat.base_url == ""

    def test_init_with_credentials(self):
        chat = litellm_Chat("anthropic/claude-sonnet-4-6", api_key="sk-test", base_url="https://proxy.example.com")
        assert chat.api_key == "sk-test"
        assert chat.base_url == "https://proxy.example.com"


class TestLiteLLMLoaderNode:
    def test_input_types_structure(self):
        inputs = litellm_loader.INPUT_TYPES()
        assert "required" in inputs
        assert "model_name" in inputs["required"]
        assert "optional" in inputs
        assert "api_key" in inputs["optional"]
        assert "base_url" in inputs["optional"]

    def test_node_metadata(self):
        assert litellm_loader.RETURN_TYPES == ("CUSTOM",)
        assert litellm_loader.FUNCTION == "chatbot"
        assert "LiteLLM" in litellm_loader.DESCRIPTION

    def test_chatbot_returns_chat_instance(self):
        loader = litellm_loader()
        (chat,) = loader.chatbot("openai/gpt-4o-mini", api_key="sk-test")
        assert isinstance(chat, litellm_Chat)
        assert chat.model_name == "openai/gpt-4o-mini"

    def test_node_class_mappings(self):
        assert "litellm_loader" in NODE_CLASS_MAPPINGS
        assert NODE_CLASS_MAPPINGS["litellm_loader"] is litellm_loader
        assert "litellm_loader" in NODE_DISPLAY_NAME_MAPPINGS


class TestCompletionKwargsBuilding:
    @mock.patch("litellm.completion")
    def test_drop_params_always_true(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert mock_completion.call_args[1]["drop_params"] is True

    @mock.patch("litellm.completion")
    def test_api_key_forwarded_when_set(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini", api_key="sk-mykey")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert mock_completion.call_args[1]["api_key"] == "sk-mykey"

    @mock.patch("litellm.completion")
    def test_api_key_omitted_when_empty(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini", api_key="")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert "api_key" not in mock_completion.call_args[1]

    @mock.patch("litellm.completion")
    def test_base_url_forwarded_when_set(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini", base_url="https://proxy.example.com")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert mock_completion.call_args[1]["api_base"] == "https://proxy.example.com"

    @mock.patch("litellm.completion")
    def test_base_url_omitted_when_empty(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini", base_url="")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert "api_base" not in mock_completion.call_args[1]

    @mock.patch("litellm.completion")
    def test_extra_parameters_forwarded(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini")
        chat.send("hello", 0.7, 100, _fresh_history(), top_p=0.9, seed=42)
        kw = mock_completion.call_args[1]
        assert kw["top_p"] == 0.9
        assert kw["seed"] == 42

    @mock.patch("litellm.completion")
    def test_model_name_passed_verbatim(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("anthropic/claude-sonnet-4-6")
        chat.send("hello", 0.7, 100, _fresh_history())
        assert mock_completion.call_args[1]["model"] == "anthropic/claude-sonnet-4-6"

    @mock.patch("litellm.completion")
    def test_temperature_and_max_tokens_forwarded(self, mock_completion):
        mock_completion.return_value = _make_response("test")
        chat = litellm_Chat("openai/gpt-4o-mini")
        chat.send("hello", 0.3, 2048, _fresh_history())
        kw = mock_completion.call_args[1]
        assert kw["temperature"] == 0.3
        assert kw["max_tokens"] == 2048


class TestNonStreamingBasic:
    @mock.patch("litellm.completion")
    def test_simple_response(self, mock_completion):
        mock_completion.return_value = _make_response("The answer is 42")
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, history, reasoning = chat.send("What is the answer?", 0.7, 100, _fresh_history())
        assert content == "The answer is 42"
        assert reasoning == ""
        assert len(history) == 3
        assert history[-1]["role"] == "assistant"
        assert history[-1]["content"] == "The answer is 42"

    @mock.patch("litellm.completion")
    def test_null_content_from_provider(self, mock_completion):
        mock_completion.return_value = _make_response(content=None)
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, history, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert content == ""
        assert history[-1]["content"] == ""

    @mock.patch("litellm.completion")
    def test_empty_string_content(self, mock_completion):
        mock_completion.return_value = _make_response(content="")
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert content == ""

    @mock.patch("litellm.completion")
    def test_reasoning_content_extracted(self, mock_completion):
        mock_completion.return_value = _make_response(reasoning_content="I think step by step", content="42")
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, reasoning = chat.send("hello", 0.7, 100, _fresh_history())
        assert content == "42"
        assert reasoning == "I think step by step"

    @mock.patch("litellm.completion")
    def test_think_tags_extracted_from_content(self, mock_completion):
        mock_completion.return_value = _make_response(content="<think>reasoning here</think>The final answer")
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, reasoning = chat.send("hello", 0.7, 100, _fresh_history())
        assert content == "The final answer"
        assert reasoning == "reasoning here"

    @mock.patch("litellm.completion")
    def test_empty_system_prompt_removed(self, mock_completion):
        mock_completion.return_value = _make_response("ok")
        chat = litellm_Chat("openai/gpt-4o-mini")
        history = [{"role": "system", "content": ""}]
        chat.send("hello", 0.7, 100, history)
        messages = mock_completion.call_args[1]["messages"]
        system_msgs = [m for m in messages if m["role"] == "system"]
        assert len(system_msgs) == 0


class TestStreamingBasic:
    @mock.patch("litellm.completion")
    def test_streaming_assembles_chunks(self, mock_completion):
        chunks = _make_stream_chunks(["Hello", " world", "!"])
        mock_completion.return_value = iter(chunks)
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, history, _ = chat.send("hello", 0.7, 100, _fresh_history(), stream=True)
        assert content == "Hello world!"
        assert history[-1]["content"] == "Hello world!"

    @mock.patch("litellm.completion")
    def test_streaming_empty_chunks(self, mock_completion):
        empty_delta = SimpleNamespace(content=None, tool_calls=None)
        empty_choice = SimpleNamespace(delta=empty_delta)
        empty_chunk = SimpleNamespace(choices=[empty_choice])
        text_delta = SimpleNamespace(content="ok", tool_calls=None)
        text_choice = SimpleNamespace(delta=text_delta)
        text_chunk = SimpleNamespace(choices=[text_choice])
        mock_completion.return_value = iter([empty_chunk, text_chunk, empty_chunk])
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history(), stream=True)
        assert content == "ok"

    @mock.patch("litellm.completion")
    def test_streaming_abrupt_termination(self, mock_completion):
        empty_chunk = SimpleNamespace(choices=[])
        mock_completion.return_value = iter([empty_chunk])
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history(), stream=True)
        assert content == ""

    @mock.patch("litellm.completion")
    def test_streaming_single_char_chunks(self, mock_completion):
        chunks = _make_stream_chunks(list("Hello"))
        mock_completion.return_value = iter(chunks)
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history(), stream=True)
        assert content == "Hello"


class TestHistoryManagement:
    @mock.patch("litellm.completion")
    def test_history_accumulates(self, mock_completion):
        mock_completion.return_value = _make_response("response1")
        chat = litellm_Chat("openai/gpt-4o-mini")
        history = _fresh_history()
        chat.send("first", 0.7, 100, history)
        assert len(history) == 3

        mock_completion.return_value = _make_response("response2")
        chat.send("second", 0.7, 100, history)
        assert len(history) == 5

    @mock.patch("litellm.completion")
    def test_history_has_user_message_before_error(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.AuthenticationError(
            message="Invalid API key", model="openai/gpt-4o-mini", llm_provider="openai"
        )
        chat = litellm_Chat("openai/gpt-4o-mini", api_key="bad-key")
        history = _fresh_history()
        chat.send("hello", 0.7, 100, history)
        assert history[-1]["role"] == "user"

    @mock.patch("litellm.completion")
    def test_img_url_creates_multimodal_message(self, mock_completion):
        mock_completion.return_value = _make_response("I see an image")
        chat = litellm_Chat("openai/gpt-4o-mini")
        chat.send("describe", 0.7, 100, _fresh_history(), img_URL="https://example.com/img.png")
        messages = mock_completion.call_args[1]["messages"]
        user_msg = messages[-1]
        assert isinstance(user_msg["content"], list)
        assert user_msg["content"][0]["type"] == "text"
        assert user_msg["content"][1]["type"] == "image_url"


# ===========================================================================
# ERROR HANDLING TESTS
# ===========================================================================


class TestErrorFormatting:
    def test_auth_error(self):
        ex = type("AuthenticationError", (Exception,), {"__module__": "litellm.exceptions"})("bad key")
        assert "[LiteLLM Auth Error]" in _format_litellm_error(ex)

    def test_not_found_error(self):
        ex = type("NotFoundError", (Exception,), {"__module__": "litellm.exceptions"})("model not found")
        assert "[LiteLLM Model Not Found]" in _format_litellm_error(ex)

    def test_rate_limit_error(self):
        ex = type("RateLimitError", (Exception,), {"__module__": "litellm.exceptions"})("429")
        assert "[LiteLLM Rate Limit]" in _format_litellm_error(ex)

    def test_timeout_error(self):
        ex = type("Timeout", (Exception,), {"__module__": "litellm.exceptions"})("timed out")
        assert "[LiteLLM Timeout]" in _format_litellm_error(ex)

    def test_context_window_error(self):
        ex = type("ContextWindowExceededError", (Exception,), {"__module__": "litellm.exceptions"})("overflow")
        assert "[LiteLLM Context Overflow]" in _format_litellm_error(ex)

    def test_connection_error(self):
        ex = type("APIConnectionError", (Exception,), {"__module__": "litellm.exceptions"})("refused")
        assert "[LiteLLM Connection Error]" in _format_litellm_error(ex)

    def test_bad_request_error(self):
        ex = type("BadRequestError", (Exception,), {"__module__": "litellm.exceptions"})("invalid")
        assert "[LiteLLM Bad Request]" in _format_litellm_error(ex)

    def test_server_error(self):
        ex = type("InternalServerError", (Exception,), {"__module__": "litellm.exceptions"})("500")
        assert "[LiteLLM Server Error]" in _format_litellm_error(ex)

    def test_generic_error_fallback(self):
        ex = ValueError("something unexpected")
        result = _format_litellm_error(ex)
        assert "[LiteLLM Error]" in result
        assert "something unexpected" in result


class TestExceptionHandlingInSend:
    @mock.patch("litellm.completion")
    def test_auth_error_returns_actionable_message(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.AuthenticationError(
            message="Incorrect API key", model="openai/gpt-4o-mini", llm_provider="openai"
        )
        chat = litellm_Chat("openai/gpt-4o-mini", api_key="sk-bad-key")
        content, _, reasoning = chat.send("hello", 0.7, 100, _fresh_history())
        assert "[LiteLLM Auth Error]" in content
        assert content == reasoning

    @mock.patch("litellm.completion")
    def test_not_found_error(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.NotFoundError(
            message="Model not found", model="nonexistent", llm_provider="openai"
        )
        chat = litellm_Chat("nonexistent")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert "[LiteLLM Model Not Found]" in content

    @mock.patch("litellm.completion")
    def test_rate_limit_error(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.RateLimitError(
            message="Rate limit reached", model="openai/gpt-4o-mini", llm_provider="openai"
        )
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert "[LiteLLM Rate Limit]" in content

    @mock.patch("litellm.completion")
    def test_context_window_exceeded(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.ContextWindowExceededError(
            message="Context too long", model="openai/gpt-4o-mini", llm_provider="openai"
        )
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert "[LiteLLM Context Overflow]" in content

    @mock.patch("litellm.completion")
    def test_timeout_error(self, mock_completion):
        import litellm as ll

        mock_completion.side_effect = ll.Timeout(
            message="Request timed out", model="openai/gpt-4o-mini", llm_provider="openai"
        )
        chat = litellm_Chat("openai/gpt-4o-mini")
        content, _, _ = chat.send("hello", 0.7, 100, _fresh_history())
        assert "[LiteLLM Timeout]" in content


# ===========================================================================
# LIVE E2E TESTS
# ===========================================================================

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_FOUNDRY_API_KEY", "")
ANTHROPIC_BASE = os.environ.get("ANTHROPIC_FOUNDRY_BASE_URL", "")
HAS_ANTHROPIC = bool(ANTHROPIC_KEY and ANTHROPIC_BASE)


def _anthropic_base_url():
    base = ANTHROPIC_BASE
    if not base.startswith("https://"):
        base = "https://" + base
    return base


@pytest.mark.skipif(not HAS_ANTHROPIC, reason="ANTHROPIC_FOUNDRY_API_KEY not set")
class TestLiveAnthropicE2E:
    def _chat(self, model="anthropic/claude-sonnet-4-6"):
        return litellm_Chat(model, api_key=ANTHROPIC_KEY, base_url=_anthropic_base_url())

    def test_live_non_streaming(self):
        content, history, _ = self._chat().send("What is 2+2? Reply with just the number.", 0.0, 50, _fresh_history())
        assert "4" in content
        assert len(history) == 3

    def test_live_streaming(self):
        content, history, _ = self._chat().send(
            "What is 3+5? Reply with just the number.", 0.0, 50, _fresh_history(), stream=True
        )
        assert "8" in content
        assert len(history) == 3

    def test_live_invalid_api_key(self):
        chat = litellm_Chat("anthropic/claude-sonnet-4-6", api_key="sk-invalid-12345", base_url=_anthropic_base_url())
        content, _, _ = chat.send("hello", 0.7, 50, _fresh_history())
        assert "[LiteLLM" in content

    def test_live_multi_turn(self):
        chat = self._chat()
        history = _fresh_history()
        chat.send("My name is Alice.", 0.0, 100, history)
        content2, _, _ = chat.send("What is my name?", 0.0, 100, history)
        assert "Alice" in content2
        assert len(history) == 5

    def test_live_bad_model_name(self):
        chat = self._chat(model="anthropic/nonexistent-xyz-999")
        content, _, _ = chat.send("hello", 0.7, 50, _fresh_history())
        assert "[LiteLLM" in content

    def test_live_drop_params_prevents_rejection(self):
        """Verify drop_params=True prevents Anthropic from rejecting OpenAI-specific params."""
        chat = self._chat()
        content, _, _ = chat.send(
            "Say OK.", 0.0, 10, _fresh_history(), seed=42, frequency_penalty=0.5, presence_penalty=0.5
        )
        assert content
        assert "[LiteLLM" not in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
