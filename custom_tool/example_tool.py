import json
import locale
from datetime import datetime

import pytz


def get_weekday(timezone):
    # 返回当前周几
    timezone = pytz.timezone(timezone)
    now = datetime.now(timezone)
    # 字符串格式输出
    weekday = now.strftime("%A")
    return weekday


class weekday_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "timezone": ("STRING", {"default": "Asia/Shanghai"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"

    def time(self, timezone, is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "get_weekday",
                    "description": "用于查询任意时区当前是星期几",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": "需要查询的时区，例如：Asia/Shanghai",
                                "default": str(timezone),
                            }
                        },
                        "required": ["timezone"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


_TOOL_HOOKS = ["get_weekday"]
NODE_CLASS_MAPPINGS = {"weekday_tool": weekday_tool}
# 获取系统语言
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
    NODE_DISPLAY_NAME_MAPPINGS = {"weekday_tool": "星期查询工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"weekday_tool": "Weekday Query Tool"}


if __name__ == "__main__":

    print(get_weekday("Asia/Shanghai"))
