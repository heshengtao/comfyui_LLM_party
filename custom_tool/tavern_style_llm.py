import base64
import configparser
import datetime
import io
import json
import locale
import os
import random
import re
import sys
import traceback

import numpy as np
import openai
from openai import AzureOpenAI, OpenAI
from PIL import Image

current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")


def _ensure_version_suffix(base_url):
    if "api.perplexity.ai" in base_url:
        return "https://api.perplexity.ai"
    match = re.search(r'/v(.+)/$', base_url)
    if not match:
        if not base_url.endswith('/'):
            base_url += '/'
        base_url += 'v1/'
    return base_url


def _normalize_kwargs(kwargs):
    normalized = dict(kwargs)
    model_name = str(normalized.get("model", "") or "").strip().lower()
    if model_name.startswith("gpt-5") and "max_completion_tokens" not in normalized and "max_tokens" in normalized:
        normalized["max_completion_tokens"] = normalized.pop("max_tokens")
    return normalized


class TavernStyleLLM:
    original_IS_CHANGED = classmethod(lambda s: float("NaN"))

    def __init__(self):
        current_time = datetime.datetime.now()
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
        temp_path = os.path.join(current_dir_path, "temp")
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        self.prompt_path = os.path.join(temp_path, f"tavern_{self.id}.json")
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump([{"role": "system", "content": ""}], f, indent=4, ensure_ascii=False)
        self.is_locked = "disable"

    @classmethod
    def INPUT_TYPES(s):
        temp_path = os.path.join(current_dir_path, "temp")
        paths = [""]
        if os.path.exists(temp_path):
            full_paths = [os.path.join(temp_path, f) for f in os.listdir(temp_path) if f.endswith(".json")]
            full_paths.sort(key=os.path.getmtime, reverse=True)
            paths += [os.path.basename(f) for f in full_paths]
        return {
            "required": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "You are a helpful assistant.",
                    "tooltip": "System prompt. Can be overridden by system_prompt_input.",
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "User prompt.",
                }),
                "model": ("CUSTOM", {"tooltip": "Model from LLM API Loader."}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
                "is_memory": (["enable", "disable"], {"default": "enable"}),
                "is_locked": (["enable", "disable"], {"default": "disable", "tooltip": "Cache output when params unchanged."}),
                "max_length": ("INT", {"default": 4096, "min": 256, "max": 128000, "step": 128}),
                "post_history_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Injected AFTER user message (SillyTavern JB position). Highest priority override.",
                }),
                "post_history_role": (["user", "system", "assistant"], {
                    "default": "user",
                    "tooltip": "Role of post-history message.",
                }),
            },
            "optional": {
                "system_prompt_input": ("STRING", {"forceInput": True, "tooltip": "Overrides/appends system_prompt from connection."}),
                "user_prompt_input": ("STRING", {"forceInput": True}),
                "file_content": ("STRING", {"forceInput": True, "tooltip": "File/RAG content appended to system prompt."}),
                "images": ("IMAGE", {"forceInput": True}),
                "imgbb_api_key": ("STRING", {"default": ""}),
                "conversation_rounds": ("INT", {"default": 100, "min": 1, "max": 10000, "step": 1}),
                "historical_record": (paths, {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "extra_parameters": ("DICT", {"forceInput": True}),
                "user_history": ("STRING", {"forceInput": True}),
                "img_URL": ("STRING", {"forceInput": True}),
                "stream": ("BOOLEAN", {"default": False}),
                "injection_prompts": ("STRING", {
                    "forceInput": True,
                    "tooltip": "JSON: [{role, content, depth}]. From Tavern Preset Loader.",
                }),
                "assistant_prefill": ("STRING", {
                    "default": "",
                    "tooltip": "Pre-fill assistant response start.",
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE", "STRING")
    RETURN_NAMES = ("assistant_response", "history", "image", "reasoning_content")
    OUTPUT_TOOLTIPS = (
        "LLM response text.",
        "Full dialogue history JSON.",
        "Images if generated.",
        "Reasoning/thinking content.",
    )
    FUNCTION = "chatbot"
    CATEGORY = "大模型派对（llm_party）/酒馆增强（tavern）"

    def chatbot(
        self,
        user_prompt,
        system_prompt,
        model,
        temperature,
        is_memory,
        is_locked,
        max_length,
        post_history_prompt="",
        post_history_role="user",
        system_prompt_input="",
        user_prompt_input="",
        file_content=None,
        images=None,
        imgbb_api_key=None,
        conversation_rounds=100,
        historical_record="",
        is_enable=True,
        extra_parameters=None,
        user_history=None,
        img_URL=None,
        stream=False,
        injection_prompts=None,
        assistant_prefill="",
    ):
        if not is_enable:
            return (None, None, None, "")

        # Merge prompt inputs
        if user_prompt is None:
            user_prompt = user_prompt_input or ""
        elif user_prompt_input:
            user_prompt = user_prompt + user_prompt_input

        if historical_record:
            self.prompt_path = os.path.join(current_dir_path, "temp", historical_record)

        if system_prompt_input:
            if system_prompt and system_prompt.strip():
                system_prompt = system_prompt + "\n\n" + system_prompt_input
            else:
                system_prompt = system_prompt_input

        # Lock handling
        self.is_locked = is_locked
        if self.is_locked == "disable":
            setattr(TavernStyleLLM, "IS_CHANGED", TavernStyleLLM.original_IS_CHANGED)
        else:
            if hasattr(TavernStyleLLM, "IS_CHANGED"):
                delattr(TavernStyleLLM, "IS_CHANGED")

        # Empty prompt: return current history
        if not user_prompt or not user_prompt.strip():
            if os.path.exists(self.prompt_path):
                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = [{"role": "system", "content": system_prompt}]
            return ("", json.dumps(history, ensure_ascii=False, indent=4), None, "")

        try:
            # Memory reset
            if is_memory == "disable" or "clear party memory" in user_prompt:
                with open(self.prompt_path, "w", encoding="utf-8") as f:
                    json.dump([{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False)
                if "clear party memory" in user_prompt:
                    return ("Memory cleared.", "[]", None, "")

            # Load history
            if os.path.exists(self.prompt_path):
                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = [{"role": "system", "content": system_prompt}]

            if user_history and user_history.strip():
                try:
                    history = json.loads(user_history)
                except:
                    pass

            # Trim to conversation_rounds
            history_temp = [history[0]]
            elements_to_keep = 2 * conversation_rounds
            if elements_to_keep < len(history) - 1:
                history_temp += history[-elements_to_keep:]
                history_copy = history[1:-elements_to_keep]
            else:
                if len(history) > 1:
                    history_temp += history[1:]
                history_copy = []
            history = history_temp

            # Update system prompt content
            for message in history:
                if message["role"] == "system":
                    message["content"] = system_prompt

            # Append file/RAG content
            if file_content:
                for message in history:
                    if message["role"] == "system":
                        message["content"] += "\n\n" + file_content

            # Remove empty system messages
            history = [m for m in history if not (m["role"] == "system" and not m.get("content", "").strip())]
            if not history or history[0]["role"] != "system":
                fallback = system_prompt if system_prompt and system_prompt.strip() else "You are a helpful assistant."
                history.insert(0, {"role": "system", "content": fallback})

            # === TAVERN-STYLE INJECTION ===

            # 1. Parse injection prompts
            inj_list = []
            if injection_prompts:
                try:
                    inj_list = json.loads(injection_prompts) if isinstance(injection_prompts, str) else injection_prompts
                except (json.JSONDecodeError, TypeError):
                    inj_list = []

            in_history_inj = [x for x in inj_list if x.get("depth", 0) > 0]
            post_history_inj = [x for x in inj_list if x.get("depth", 0) <= 0]

            # 2. Insert in-history injections (depth > 0, deepest first)
            _role_pri = {"system": 0, "user": 1, "assistant": 2}
            depth_groups = {}
            for inj in in_history_inj:
                depth_groups.setdefault(inj["depth"], []).append(inj)

            for depth in sorted(depth_groups.keys(), reverse=True):
                group = depth_groups[depth]
                group.sort(key=lambda x: (-x.get("order", 100), _role_pri.get(x.get("role", "system"), 0)))
                pos = max(1, len(history) - depth)
                for inj in reversed(group):
                    history.insert(pos, {"role": inj["role"], "content": inj["content"]})

            # 3. User message (with optional images)
            final_user_content = user_prompt
            if images is not None:
                img_json = [{"type": "text", "text": user_prompt}]
                for image in images:
                    i = 255.0 * image.cpu().numpy()
                    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    if imgbb_api_key:
                        import requests
                        resp = requests.post("https://api.imgbb.com/1/upload", data={"key": imgbb_api_key, "image": img_str})
                        if resp.status_code == 200:
                            img_json.append({"type": "image_url", "image_url": {"url": resp.json()["data"]["url"]}})
                    else:
                        img_json.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}})
                final_user_content = img_json
            elif img_URL:
                final_user_content = [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": img_URL}},
                ]

            history.append({"role": "user", "content": final_user_content})

            # 4. Post-history injections (depth=0 from injection_prompts)
            post_history_inj.sort(key=lambda x: (-x.get("order", 100), _role_pri.get(x.get("role", "system"), 0)))
            for inj in post_history_inj:
                history.append({"role": inj["role"], "content": inj["content"]})

            # 5. Manual post-history prompt (for use without PresetLoader)
            if post_history_prompt and post_history_prompt.strip():
                history.append({"role": post_history_role, "content": post_history_prompt})

            # 6. Assistant prefill
            if assistant_prefill and assistant_prefill.strip():
                history.append({"role": "assistant", "content": assistant_prefill})

            # Handle o1/o3 models: swap system role to user
            model_name = getattr(model, "model_name", "")
            if re.search(r'o[1-3]', model_name):
                for i in range(len(history)):
                    if history[i]["role"] == "system":
                        history[i]["role"] = "user"
                        history.insert(i + 1, {"role": "assistant", "content": "OK"})
                        break

            # Remove empty messages (API rejects empty content blocks)
            history = [
                m for m in history
                if (isinstance(m.get("content"), list)) or
                   (isinstance(m.get("content"), str) and m["content"].strip())
            ]

            # === API CALL ===
            print("[TavernStyleLLM] Sending messages:")
            for i, m in enumerate(history):
                role = m.get("role", "?")
                content = m.get("content", "")
                if isinstance(content, list):
                    content = "[multimodal]"
                preview = content[:60] + "..." if len(content) > 60 else content
                preview = preview.replace("\n", " ")
                print(f"  [{i}] {role}: {preview}")

            apikey = getattr(model, "apikey", "")
            baseurl = _ensure_version_suffix(getattr(model, "baseurl", ""))

            if "api.perplexity.ai" in baseurl:
                client = OpenAI(api_key=apikey, base_url="https://api.perplexity.ai")
            elif "openai.azure.com" in baseurl:
                api_version = baseurl.split("=")[-1].split("/")[0]
                azure_endpoint = "https://" + baseurl.split("//")[1].split("/")[0]
                client = AzureOpenAI(api_key=apikey, api_version=api_version, azure_endpoint=azure_endpoint)
            else:
                client = OpenAI(api_key=apikey, base_url=baseurl)

            call_kwargs = _normalize_kwargs({
                "model": model_name,
                "messages": history,
                "temperature": temperature,
                "max_tokens": int(max_length),
                "stream": stream,
            })
            if extra_parameters:
                call_kwargs.update(extra_parameters)

            response = client.chat.completions.create(**call_kwargs)

            reasoning_content = ""
            response_content = ""

            if stream:
                for chunk in response:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                            print(delta.reasoning_content, end="", flush=True)
                            reasoning_content += delta.reasoning_content
                        elif hasattr(delta, "content") and delta.content:
                            print(delta.content, end="", flush=True)
                            response_content += delta.content
            else:
                msg = response.choices[0].message
                if hasattr(msg, "reasoning_content") and msg.reasoning_content:
                    reasoning_content = msg.reasoning_content
                response_content = msg.content or ""

            # Extract <think> blocks
            think_match = re.search(r"<think>(.*?)</think>", response_content, re.DOTALL)
            if think_match:
                reasoning_content = think_match.group(1).strip()
                response_content = response_content.replace(think_match.group(0), "").strip()

            # Prepend prefill to response
            if assistant_prefill and assistant_prefill.strip():
                response_content = assistant_prefill + response_content

            # === SAVE HISTORY (persistent, without transient injections) ===
            # Collect content strings of injected messages to filter them out
            transient_contents = set()
            for inj in inj_list:
                transient_contents.add(inj.get("content", ""))
            if post_history_prompt and post_history_prompt.strip():
                transient_contents.add(post_history_prompt)
            if assistant_prefill and assistant_prefill.strip():
                transient_contents.add(assistant_prefill)

            save_history = []
            seen_system = False
            for m in history:
                if m.get("role") == "system":
                    if seen_system:
                        continue
                    seen_system = True
                elif m.get("content") in transient_contents:
                    continue
                save_history.append(m)

            # Add assistant response
            save_history.append({"role": "assistant", "content": response_content})

            # Merge back the trimmed older history
            full_history = [save_history[0]]
            full_history.extend(history_copy)
            full_history.extend(save_history[1:])

            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(full_history, f, indent=4, ensure_ascii=False)

            history_str = json.dumps(full_history, ensure_ascii=False, indent=4)

            return (response_content, history_str, None, reasoning_content)

        except Exception as ex:
            traceback.print_exc()
            return (str(ex), str(ex), None, "")


NODE_CLASS_MAPPINGS = {"TavernStyleLLM": TavernStyleLLM}

lang = "zh_CN"
try:
    system_lang = locale.getlocale()[0]
    if system_lang and system_lang.lower().startswith("en"):
        lang = "en_US"
except Exception:
    pass

config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language in ("zh_CN", "en_US"):
    lang = language

if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"TavernStyleLLM": "酒馆风格LLM"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"TavernStyleLLM": "Tavern Style LLM"}
