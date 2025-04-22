import webbrowser
import json
import locale

class open_url_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path_or_url": ("STRING", {"default": "https://github.com/heshengtao/comfyui_LLM_party"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log",)
    OUTPUT_NODE = True
    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def convert_txt2json(self,path_or_url, is_enable=True):
        if is_enable == False:
            return (None,)
        print(os.environ.get('BROWSER'))
        try:
            success = webbrowser.open(path_or_url)
            if success:
                return "成功打开网页"
            else:
                return "无法打开网页"
        except Exception as e:
            return f"打开网页时出错: {str(e)}"

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

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"

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
    "open_url_function": open_url_function,
    }
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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "open_url_tool": "打开网页工具",
        "open_url_function": "打开网页",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "open_url_tool": "Open Web tool",
        "open_url_function": "Open Web",
        }