import base64
import io
import json
import os
import re

import numpy as np
import requests
from PIL import Image

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


DEFAULT_BASE_URL = "https://global.api-route.com/v1"
DEFAULT_MODEL = "claude-sonnet-4-5"

SUPPORTED_MODELS = [
    "claude-sonnet-4-5",
    "claude-haiku-4-5",
    "claude-opus-4-1",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "o3-mini",
    "deepseek-chat",
    "deepseek-reasoner",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "qwen-2.5-72b-instruct",
]


def _format_api_route_error(ex):
    qualname = f"{type(ex).__module__}.{type(ex).__qualname__}"
    msg = str(ex)

    if "AuthenticationError" in qualname:
        return f"[API Route Auth Error] Invalid or missing API key. Please check your API Route key from https://www.api-route.com. Detail: {msg}"
    if "NotFoundError" in qualname:
        return f"[API Route Model Not Found] Model name may be invalid or unsupported. Detail: {msg}"
    if "RateLimitError" in qualname:
        return f"[API Route Rate Limit] Rate limit reached. Please retry shortly. Detail: {msg}"
    if "APIConnectionError" in qualname:
        return f"[API Route Connection Error] Could not connect to API Route endpoint. Check base_url and network. Detail: {msg}"
    return f"[API Route Error] {msg}"


class api_route_Chat:
    def __init__(self, model_name=DEFAULT_MODEL, api_key="", base_url=DEFAULT_BASE_URL) -> None:
        self.model_name = model_name or DEFAULT_MODEL
        self.api_key = api_key or os.environ.get("API_ROUTE_API_KEY", "")
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        if not self.base_url.endswith("/v1"):
            self.base_url = f"{self.base_url}/v1"

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
        if OpenAI is None:
            return (
                "Error: openai library is not installed. Please run: pip install openai",
                history,
                "",
            )

        try:
            client = OpenAI(
                api_key=self.api_key or "sk-dummy",
                base_url=self.base_url,
            )

            # Process images if any
            if images is not None and (img_URL is None or img_URL == ""):
                try:
                    from ..config import config_path, load_api_keys
                    if not imgbb_api_key:
                        api_keys = load_api_keys(config_path)
                        imgbb_api_key = api_keys.get("imgbb_api")
                except Exception:
                    pass

                if not imgbb_api_key:
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
                    user_prompt = img_json
            elif img_URL:
                user_prompt = [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": img_URL}},
                ]

            history.append({"role": "user", "content": user_prompt})

            completion_kwargs = {
                "model": self.model_name,
                "messages": history,
                "temperature": float(temperature) if temperature is not None else 0.7,
                "max_tokens": int(max_length) if max_length else 4096,
                "stream": bool(stream),
            }

            if tools and is_tools_in_sys_prompt == "disable":
                completion_kwargs["tools"] = tools

            # Optional extra parameters (seed, etc.)
            for k, v in extra_parameters.items():
                if v is not None and k not in completion_kwargs:
                    completion_kwargs[k] = v

            response_content = ""
            reasoning_content = ""

            if stream:
                response = client.chat.completions.create(**completion_kwargs)
                for chunk in response:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                            reasoning_content += delta.reasoning_content
                        elif hasattr(delta, "content") and delta.content:
                            response_content += delta.content
            else:
                response = client.chat.completions.create(**completion_kwargs)
                choice = response.choices[0]
                if hasattr(choice.message, "reasoning_content") and choice.message.reasoning_content:
                    reasoning_content = choice.message.reasoning_content
                response_content = choice.message.content or ""

            if isinstance(response_content, str):
                pattern = r"<think>(.*?)</think>"
                match = re.search(pattern, response_content, re.DOTALL)
                if match:
                    reasoning_content = match.group(1).strip()
                    response_content = response_content.replace(match.group(0), "").strip()

            history.append({"role": "assistant", "content": str(response_content)})
            return response_content, history, reasoning_content

        except Exception as ex:
            response_content = _format_api_route_error(ex)
            reasoning_content = response_content
            return response_content, history, reasoning_content


class api_route_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (
                    SUPPORTED_MODELS,
                    {
                        "default": DEFAULT_MODEL,
                        "tooltip": (
                            "API Route model name. Supports leading models from Claude, OpenAI, DeepSeek, Gemini, etc."
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
                            "API Route API key (sk-...). Get your key from https://www.api-route.com"
                        ),
                    },
                ),
                "base_url": (
                    "STRING",
                    {
                        "default": DEFAULT_BASE_URL,
                        "tooltip": (
                            "API Route base URL (default: https://global.api-route.com/v1)."
                        ),
                    },
                ),
                "custom_model": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": (
                            "Optional custom model identifier if not listed in the presets."
                        ),
                    },
                ),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    OUTPUT_TOOLTIPS = ("The loaded API Route model.",)
    DESCRIPTION = "Load models via API Route (https://www.api-route.com). High-concurrency AI gateway offering Claude, GPT-4o, DeepSeek, Gemini, and open models."
    FUNCTION = "chatbot"
    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def chatbot(self, model_name, api_key="", base_url=DEFAULT_BASE_URL, custom_model=""):
        selected_model = custom_model.strip() if custom_model and custom_model.strip() else model_name
        chat = api_route_Chat(selected_model, api_key=api_key, base_url=base_url)
        return (chat,)


NODE_CLASS_MAPPINGS = {
    "api_route_loader": api_route_loader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "api_route_loader": "⚡API Route Loader",
}
