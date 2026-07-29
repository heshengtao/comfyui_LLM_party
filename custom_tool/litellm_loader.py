import base64
import io
import json
import re

import numpy as np
import requests
from PIL import Image


def _format_litellm_error(ex):
    """Return a user-facing error string with actionable guidance based on the litellm exception type."""
    qualname = f"{type(ex).__module__}.{type(ex).__qualname__}"
    msg = str(ex)

    if "AuthenticationError" in qualname:
        return f"[LiteLLM Auth Error] Invalid or missing API key. Check your api_key or provider env var. Detail: {msg}"
    if "NotFoundError" in qualname:
        return f"[LiteLLM Model Not Found] Model name may be wrong or unsupported. Use provider/model format (e.g. openai/gpt-4o-mini). Detail: {msg}"
    if "RateLimitError" in qualname:
        return (
            f"[LiteLLM Rate Limit] Provider rate limit hit. Wait and retry, or use a different model/key. Detail: {msg}"
        )
    if "Timeout" in qualname:
        return f"[LiteLLM Timeout] Request timed out. Check your network or increase timeout. Detail: {msg}"
    if "ContextWindowExceededError" in qualname or "context_length_exceeded" in msg.lower():
        return f"[LiteLLM Context Overflow] Input exceeds model's context window. Reduce message history or max_tokens. Detail: {msg}"
    if "ServiceUnavailableError" in qualname or "InternalServerError" in qualname:
        return f"[LiteLLM Server Error] Provider returned a server error. Try again later. Detail: {msg}"
    if "BadRequestError" in qualname:
        return f"[LiteLLM Bad Request] The request was rejected by the provider. Detail: {msg}"
    if "APIConnectionError" in qualname:
        return f"[LiteLLM Connection Error] Could not connect to the provider API. Check base_url and network. Detail: {msg}"
    return f"[LiteLLM Error] {msg}"


class litellm_Chat:
    def __init__(self, model_name, api_key="", base_url="") -> None:
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def send(
        self,
        user_prompt,
        temperature,
        max_length,
        history,
        tools=None,
        is_tools_in_sys_prompt="disable",
        images=None,
        imgbb_api_key="",
        img_URL=None,
        stream=False,
        **extra_parameters,
    ):
        try:
            import litellm
        except ImportError:
            return (
                "Error: litellm is not installed. Please run: pip install litellm",
                history,
                "",
            )

        try:
            if images is not None and (img_URL is None or img_URL == ""):
                from ..config import config_path, load_api_keys

                if imgbb_api_key == "" or imgbb_api_key is None:
                    api_keys = load_api_keys(config_path)
                    imgbb_api_key = api_keys.get("imgbb_api")
                if imgbb_api_key == "" or imgbb_api_key is None:
                    img_json = [{"type": "text", "text": user_prompt}]
                    for image in images:
                        i = 255.0 * image.cpu().numpy()
                        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        img_json.append(
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{img_str}"},
                            }
                        )
                    user_prompt = img_json
                else:
                    img_json = [{"type": "text", "text": user_prompt}]
                    for image in images:
                        i = 255.0 * image.cpu().numpy()
                        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        url = "https://api.imgbb.com/1/upload"
                        payload = {"key": imgbb_api_key, "image": img_str}
                        resp = requests.post(url, data=payload)
                        if resp.status_code == 200:
                            result = resp.json()
                            img_url = result["data"]["url"]
                            img_json.append(
                                {
                                    "type": "image_url",
                                    "image_url": {"url": img_url},
                                }
                            )
                        else:
                            return (
                                "Error uploading image to imgbb: " + resp.text,
                                history,
                                "",
                            )
                    user_prompt = img_json
            elif img_URL is not None and img_URL != "":
                user_prompt = [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": img_URL}},
                ]

            for i in range(len(history)):
                if history[i]["role"] == "system" and history[i]["content"] == "":
                    history.pop(i)
                    break

            new_message = {"role": "user", "content": user_prompt}
            history.append(new_message)
            print(history)
            reasoning_content = ""

            completion_kwargs = {
                "model": self.model_name,
                "messages": history,
                "temperature": temperature,
                "max_tokens": max_length,
                "drop_params": True,
                "stream": stream,
                **extra_parameters,
            }
            if self.api_key:
                completion_kwargs["api_key"] = self.api_key
            if self.base_url:
                completion_kwargs["api_base"] = self.base_url

            if tools is not None:
                completion_kwargs["tools"] = tools
                response = litellm.completion(**completion_kwargs)
                if stream:
                    tool_calls = []
                    response_content = ""
                    reasoning_content = ""
                    for chunk in response:
                        if chunk.choices:
                            choice = chunk.choices[0]
                            if choice.delta.tool_calls:
                                for idx, tool_call in enumerate(choice.delta.tool_calls):
                                    tool = choice.delta.tool_calls[idx]
                                    if len(tool_calls) <= idx:
                                        tool_calls.append(tool)
                                        continue
                                    if tool.function.arguments:
                                        tool_calls[idx].function.arguments += tool.function.arguments
                            else:
                                if (
                                    hasattr(chunk.choices[0].delta, "reasoning_content")
                                    and chunk.choices[0].delta.reasoning_content
                                ):
                                    print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                                    reasoning_content += chunk.choices[0].delta.reasoning_content
                                elif hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                                    print(chunk.choices[0].delta.content, end="", flush=True)
                                    response_content += chunk.choices[0].delta.content
                    while tool_calls:
                        response_content = tool_calls[0].function
                        print("Calling tool: " + response_content.name)
                        print(response_content.arguments)
                        from ..llm import dispatch_tool

                        results = dispatch_tool(response_content.name, json.loads(response_content.arguments))
                        print(results)
                        history.append(
                            {
                                "tool_calls": [
                                    {
                                        "id": tool_calls[0].id,
                                        "function": {
                                            "arguments": response_content.arguments,
                                            "name": response_content.name,
                                        },
                                        "type": tool_calls[0].type,
                                    }
                                ],
                                "role": "assistant",
                                "content": str(response_content),
                            }
                        )
                        history.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_calls[0].id,
                                "name": response_content.name,
                                "content": results,
                            }
                        )
                        completion_kwargs["messages"] = history
                        response = litellm.completion(**completion_kwargs)
                        tool_calls = []
                        response_content = ""
                        reasoning_content = ""
                        for chunk in response:
                            if chunk.choices:
                                choice = chunk.choices[0]
                                if choice.delta.tool_calls:
                                    for idx, tool_call in enumerate(choice.delta.tool_calls):
                                        tool = choice.delta.tool_calls[idx]
                                        if len(tool_calls) <= idx:
                                            tool_calls.append(tool)
                                            continue
                                        if tool.function.arguments:
                                            tool_calls[idx].function.arguments += tool.function.arguments
                                else:
                                    if (
                                        hasattr(chunk.choices[0].delta, "reasoning_content")
                                        and chunk.choices[0].delta.reasoning_content
                                    ):
                                        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                                        reasoning_content += chunk.choices[0].delta.reasoning_content
                                    elif hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                                        print(chunk.choices[0].delta.content, end="", flush=True)
                                        response_content += chunk.choices[0].delta.content
                else:
                    response_content = response.choices[0].message.content or ""
                    print(response_content)
                    while response.choices[0].message.tool_calls:
                        assistant_message = response.choices[0].message
                        response_content = assistant_message.tool_calls[0].function
                        print("Calling tool: " + response_content.name)
                        print(response_content.arguments)
                        from ..llm import dispatch_tool

                        results = dispatch_tool(response_content.name, json.loads(response_content.arguments))
                        print(results)
                        history.append(
                            {
                                "tool_calls": [
                                    {
                                        "id": assistant_message.tool_calls[0].id,
                                        "function": {
                                            "arguments": response_content.arguments,
                                            "name": response_content.name,
                                        },
                                        "type": assistant_message.tool_calls[0].type,
                                    }
                                ],
                                "role": "assistant",
                                "content": str(response_content),
                            }
                        )
                        history.append(
                            {
                                "role": "tool",
                                "tool_call_id": assistant_message.tool_calls[0].id,
                                "name": response_content.name,
                                "content": results,
                            }
                        )
                        completion_kwargs["messages"] = history
                        response = litellm.completion(**completion_kwargs)
                        if (
                            hasattr(response.choices[0].message, "reasoning_content")
                            and response.choices[0].message.reasoning_content
                        ):
                            reasoning_content = response.choices[0].message.reasoning_content
                            print(reasoning_content)
                        response_content = response.choices[0].message.content or ""
                        print(response_content)
            elif is_tools_in_sys_prompt == "enable":
                del completion_kwargs["stream"]
                response = litellm.completion(**completion_kwargs)
                response_content = response.choices[0].message.content or ""
                pattern = r'\{\s*"tool":\s*"(.*?)",\s*"parameters":\s*\{(.*?)\}\s*\}'
                while re.search(pattern, response_content, re.DOTALL) is not None:
                    match = re.search(pattern, response_content, re.DOTALL)
                    tool = match.group(1)
                    parameters = match.group(2)
                    json_str = '{"tool": "' + tool + '", "parameters": {' + parameters + "}}"
                    print("Calling tool: " + tool)
                    parameters = json.loads("{" + parameters + "}")
                    from ..llm import dispatch_tool

                    results = dispatch_tool(tool, parameters)
                    print(results)
                    history.append({"role": "assistant", "content": json_str})
                    history.append(
                        {
                            "role": "user",
                            "content": (
                                "The tool "
                                + tool
                                + " returned: "
                                + results
                                + ". Please answer the question based on this result."
                            ),
                        }
                    )
                    completion_kwargs["messages"] = history
                    response = litellm.completion(**completion_kwargs)
                    if (
                        hasattr(response.choices[0].message, "reasoning_content")
                        and response.choices[0].message.reasoning_content
                    ):
                        reasoning_content = response.choices[0].message.reasoning_content
                        print(reasoning_content)
                    response_content = response.choices[0].message.content or ""
                    print(response_content)
            else:
                response = litellm.completion(**completion_kwargs)
                response_content = ""
                reasoning_content = ""
                if stream:
                    for chunk in response:
                        if chunk.choices:
                            if (
                                hasattr(chunk.choices[0].delta, "reasoning_content")
                                and chunk.choices[0].delta.reasoning_content
                            ):
                                print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                                reasoning_content += chunk.choices[0].delta.reasoning_content
                            elif hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                                print(chunk.choices[0].delta.content, end="", flush=True)
                                response_content += chunk.choices[0].delta.content
                    print(response_content)
                else:
                    if (
                        hasattr(response.choices[0].message, "reasoning_content")
                        and response.choices[0].message.reasoning_content
                    ):
                        reasoning_content = response.choices[0].message.reasoning_content
                        print(reasoning_content)
                    response_content = response.choices[0].message.content or ""
                    print(response_content)

            if isinstance(response_content, str):
                pattern = r"<think>(.*?)</think>"
                match = re.search(pattern, response_content, re.DOTALL)
                if match:
                    reasoning_content = match.group(1).strip()
                    response_content = response_content.replace(match.group(0), "").strip()
            history.append({"role": "assistant", "content": str(response_content)})
        except Exception as ex:
            response_content = _format_litellm_error(ex)
            reasoning_content = response_content
        return response_content, history, reasoning_content


class litellm_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (
                    "STRING",
                    {
                        "default": "openai/gpt-4o-mini",
                        "tooltip": (
                            "LiteLLM model name in provider/model format. Examples: openai/gpt-4o-mini, anthropic/claude-sonnet-4-6, azure/my-deployment, bedrock/anthropic.claude-3-haiku, ollama/llama3. See https://docs.litellm.ai/docs/providers for all supported providers."
                        ),
                    },
                ),
            },
            "optional": {
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": (
                            "API key for the provider. If empty, LiteLLM reads from environment variables (e.g. OPENAI_API_KEY, ANTHROPIC_API_KEY)."
                        ),
                    },
                ),
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": (
                            "Custom API base URL. Use this to point at a LiteLLM proxy server or self-hosted endpoint."
                        ),
                    },
                ),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    OUTPUT_TOOLTIPS = ("The loaded LiteLLM model.",)
    DESCRIPTION = "Load any LLM via LiteLLM AI gateway. Supports 100+ providers (OpenAI, Anthropic, Azure, Bedrock, Vertex, Ollama, etc.) through a unified interface. Install with: pip install litellm"
    FUNCTION = "chatbot"

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def chatbot(self, model_name, api_key="", base_url=""):
        chat = litellm_Chat(model_name, api_key=api_key, base_url=base_url)
        return (chat,)


NODE_CLASS_MAPPINGS = {
    "litellm_loader": litellm_loader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "litellm_loader": "☁️LiteLLM Loader",
}
