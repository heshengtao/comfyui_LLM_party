import json
import locale

class custom_persona_v2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "根据背景知识，请帮我写一篇关于{主题}的文章。",
                    },
                ),
                "prompt_template": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": '{"主题":"人工智能"}',
                    },
                ),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("system_prompt",)

    FUNCTION = "custom"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def custom(self, prompt, prompt_template, is_enable=True, file_content=None):
        if is_enable == False:
            return (None,)
        # 去除prompt_template中的转义符
        prompt_template = prompt_template.replace("\\", "")
        prompt_template=json.loads(prompt_template)
        prompt = prompt.format(**prompt_template)
        text = ""
        if file_content is not None:
            text = "## 背景知识：\n" + file_content + "\n\n"
        sys_prompt = (
            text
            +
            "## 要求：\n" 
            +
            prompt
        )
        sys_prompt = sys_prompt.strip()
        return (sys_prompt,)

NODE_CLASS_MAPPINGS = {"custom_persona_v2": custom_persona_v2}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"custom_persona_v2": "自定义面具V2"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"custom_persona_v2": "custom persona v2"}