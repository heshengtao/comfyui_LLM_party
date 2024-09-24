import webbrowser
import json
import locale
def open_url(url):
    # 用默认浏览器打开URL
    try:
        webbrowser.open(url)
    except Exception as e:
        return f"打开网页时出错: {str(e)}"
    return "成功打开网页"

class open_url_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def convert_txt2json(self, is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "open_url",
                    "description": "打开指定的URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "要打开的URL"},
                        },
                        "required": ["url"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
    
_TOOL_HOOKS = ["open_url"]
NODE_CLASS_MAPPINGS = {
    "open_url_tool": open_url_tool,
    }
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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "open_url_tool": "打开网页工具",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "open_url_tool": "Open Web tool",
        }