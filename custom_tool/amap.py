import json
import locale
import requests

amap_api_key = ""
def get_amap_weather(city_code):
    global amap_api_key
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': amap_api_key,
        'city': city_code,
        'extensions': 'all'  # 'base' for current weather, 'all' for forecast
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

class AmapWeatherTool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "city_code": ("STRING", {"default": "110000"}),  # 默认北京市编码
                "api_key": ("STRING", {"default": "你的高德API密钥"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "amap_weather"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def amap_weather(self, city_code, api_key, is_enable=True):
        if not is_enable:
            return (None,)
        global amap_api_key
        amap_api_key = api_key
        weather_info = get_amap_weather(city_code, api_key)
        if weather_info:
            output = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_amap_weather",
                        "description": "用于查询指定城市的天气信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city_code": {
                                    "type": "string",
                                    "description": "需要查询的城市编码，例如：110000（北京）",
                                    "default": str(city_code),
                                }
                            },
                            "required": ["city_code"],
                        },
                    },
                }
            ]
            out = json.dumps(output, ensure_ascii=False)
            return (out,)
        else:
            return (None,)

_TOOL_HOOKS = ["get_amap_weather"]
NODE_CLASS_MAPPINGS = {"AmapWeatherTool": AmapWeatherTool}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"AmapWeatherTool": "高德天气查询工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"AmapWeatherTool": "Amap Weather Query Tool"}