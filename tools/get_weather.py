import json
import requests


class FreeApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_result(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.text
        else:
            return None


def get_weather(city,extensions="all"):
    api = FreeApi('https://tools.mgtv100.com/external/v1/weathers/query?city='+city+'&extensions='+extensions+'&output=JSON')
    result = api.get_result()
    if result:
        if extensions=="all":
            data = json.loads(result)
            return "查询到的天气信息如下："+str(data ['data']['forecasts'])+"请根据天气信息回答用户问题"
        if extensions=="base":
            data = json.loads(result)
            return "查询到的天气信息如下："+str(data ['data']['lives'])+"请根据天气信息回答用户问题"
        
class weather_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "city": ("STRING", {
                    "default": "上海市"
                }),
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),  
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "weather"

    #OUTPUT_NODE = False

    CATEGORY = "llm/工具（tools）"



    def weather(self,city,is_enable="enable"):
        if is_enable=="disable":
            return (None,)   
        output=    [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获得查询目标区域当前/未来的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "用户询问的目标区域，例如：长沙市，默认查询"+city
                    },
                    "extensions": {
                        "type": "string",
                        "description": "可选值：base/all base:返回实况天气 all:返回预报天气，默认为all "
                    }
                },
                "required": ["city"]
            }
        }
    }]
        out=json.dumps(output, ensure_ascii=False)
        return (out,)