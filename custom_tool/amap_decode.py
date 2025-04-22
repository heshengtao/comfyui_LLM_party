import json
import locale

amap_api_key = ""
import requests
def get_amap_regeo(location, extensions="all", radius=1000):
    global amap_api_key

    url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        'key': amap_api_key,
        'location': location,
        'extensions': extensions,
        'radius': str(radius)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

class AmapRegeoTool:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "location": ("STRING", {"default": "116.310003,39.991957"}),  # 默认位置坐标
                "api_key": ("STRING", {"default": "你的高德API密钥"}),
                "extensions": ("STRING", {"default": "all"}),
                "radius": ("INTEGER", {"default": 1000}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "amap_regeo"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def amap_regeo(self, location, api_key, extensions="all", radius=1000, is_enable=True):
        if not is_enable:
            return (None,)
        global amap_api_key
        amap_api_key = api_key
        regeo_info = get_amap_regeo(location, api_key, extensions, radius)
        if regeo_info:
            output = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_amap_regeo",
                        "description": "用于根据坐标获取逆地理编码信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "需要查询的经纬度坐标，例如：116.310003,39.991957",
                                    "default": str(location),
                                },
                                "extensions": {
                                    "type": "string",
                                    "description": "返回结果控制",
                                    "default": str(extensions),
                                },
                                "radius": {
                                    "type": "integer",
                                    "description": "搜索半径（单位：米）",
                                    "default": radius,
                                }
                            },
                            "required": ["location"],
                        },
                    },
                }
            ]
            out = json.dumps(output, ensure_ascii=False)
            return (out,)
        else:
            return (None,)

_TOOL_HOOKS = ["get_amap_regeo"]
NODE_CLASS_MAPPINGS = {"AmapRegeoTool": AmapRegeoTool}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"AmapRegeoTool": "高德逆地理编码工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"AmapRegeoTool": "Amap Reverse Geocoding Tool"}