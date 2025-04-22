import json
import re
import locale
def replace_keys_in_string(s, key_values):

    # 使用正则表达式找到所有的 {key} 模式
    keys = re.findall(r'\{(.*?)\}', s)
    # 对找到的每一个键，如果存在于字典中，则替换；否则忽略它
    for key in keys:
        if key in key_values:
            s = s.replace('{' + key + '}', str(key_values[key]))
    return s

class custom_string_format:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "string": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "请帮我写一篇关于{主题}的文章。",
                    },
                ),
                "string_template": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": '{"主题":"人工智能"}',
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("format_string",)

    FUNCTION = "custom"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/文本（text）"

    def custom(self, string, string_template, is_enable=True):
        if is_enable == False:
            return (None,)
        string_template=json.loads(string_template)
        string = replace_keys_in_string(string, string_template)
        format_string = string.strip()
        return (format_string,)
    
NODE_CLASS_MAPPINGS = {"custom_string_format": custom_string_format}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'

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
    NODE_DISPLAY_NAME_MAPPINGS = {"custom_string_format": "自定义字符串格式化"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"custom_string_format": "Custom String Format"}