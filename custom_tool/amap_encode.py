import json
import locale
import requests

amap_api_key = ""
def geocode(address):
    global amap_api_key
    # 调用地理编码API
    url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={amap_api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1' and data['geocodes']:
        location = data['geocodes'][0]['location']
        return location
    else:
        return None


class GeocodeTool:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "address": ("STRING", {"default": "北京市朝阳区阜通东大街6号"}),
                "api_key": ("STRING", {"default": "你的高德API密钥"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "geocode"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def geocode(self, address, api_key, is_enable=True):
        if not is_enable:
            return (None,)
        global amap_api_key
        amap_api_key = api_key
        output = [
            {
                "type": "function",
                "function": {
                    "name": "geocode",
                    "description": "用于将地址转换为地理坐标",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "需要查询的地址，例如：北京市朝阳区",
                                "default": str(address),
                            }
                        },
                        "required": ["address"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


_TOOL_HOOKS = ["geocode"]
NODE_CLASS_MAPPINGS = {"GeocodeTool": GeocodeTool}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"GeocodeTool": "高德地理编码工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"GeocodeTool": "Amap Geocode Tool"}
