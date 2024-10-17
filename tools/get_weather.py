import json

import requests

accuweather_key_load = ""


class FreeApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_result(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.text
        else:
            return None


def get_accuweather(city, extensions="all"):
    global accuweather_key_load
    if accuweather_key_load == "":
        return "请先在工具（tools）中输入accuweather的key"
    # 查询城市位置Key
    api = FreeApi(
        "http://dataservice.accuweather.com/locations/v1/cities/search?apikey="
        + accuweather_key_load
        + "&q="
        + city
        + "&language=zh-CN&details=false"
    )
    result = api.get_result()
    # 根据key查天气
    if result:
        data = json.loads(result)
        city_key = data[0]["Key"]
        # 查询实时天气
        if extensions == "all":
            api = FreeApi(
                "http://dataservice.accuweather.com/currentconditions/v1/"
                + city_key
                + "?apikey="
                + accuweather_key_load
                + "&language=zh-CN&details=false"
            )
        # 查询未来天气
        if extensions == "base":
            api = FreeApi(
                "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
                + city_key
                + "?apikey="
                + accuweather_key_load
                + "&language=zh-CN&details=false"
            )
    # 返回天气信息
    result = api.get_result()
    if result:
        if extensions == "all":
            data = json.loads(result)
            return "查询到的天气信息如下：" + str(data[0]) + "请根据天气信息回答用户问题"
        if extensions == "base":
            data = json.loads(result)
            return "查询到的天气信息如下：" + str(data["DailyForecasts"]) + "请根据天气信息回答用户问题"


class accuweather_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "city": ("STRING", {"default": "上海市"}),
                "accuweather_key": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "weather"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"

    def weather(self, accuweather_key, city, is_enable=True):
        if is_enable == False:
            return (None,)
        global accuweather_key_load
        accuweather_key_load = accuweather_key
        output = [
            {
                "type": "function",
                "function": {
                    "name": "get_accuweather",
                    "description": "获得查询目标区域当前/未来的天气情况",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市，例如：长沙市",
                                "default": city,
                            },
                            "extensions": {
                                "type": "string",
                                "description": "可选值：base/all base:返回实况天气 all:返回预报天气 ",
                                "default": "all",
                            },
                        },
                        "required": ["city"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
