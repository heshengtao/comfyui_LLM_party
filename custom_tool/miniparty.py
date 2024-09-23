import configparser
import json
import locale
import os

import openai

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")
def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


class mini_party:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "prompt": ("STRING", {"default": "input function here","multiline": True}),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        prompt,
        model_name,
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        history= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_str}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output = response.choices[0].message.content
        return (output,)
    
NODE_CLASS_MAPPINGS = {"mini_party": mini_party}
# 获取系统语言
lang = locale.getdefaultlocale()[0]
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"mini_party": "迷你派对"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"mini_party": "Mini-Party"}