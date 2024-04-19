import ast
import json
import pytz

def get_time(timezone):
    from datetime import datetime
    datetime = datetime.now(pytz.timezone(timezone))
    return f"当前日期和时间：{datetime}"


class time_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "timezone": ("STRING", {
                    "default": "Asia/Shanghai"
                }),
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),  
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "time"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"



    def time(self, timezone,is_enable="enable"):
        if is_enable=="disable":
            return (None,)        
        output=    [{
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "用于查询任意时区的时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "需要查询的时区，例如：Asia/Shanghai，默认查询"+str(timezone)
                    }
                },
                "required": ["timezone"]
            }
        }
    }]
        out=json.dumps(output, ensure_ascii=False)
        return (out,)
    
if __name__ == '__main__':
    print(time_tool().time("Asia/Shanghai"))