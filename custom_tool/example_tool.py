import json
from datetime import datetime

import pytz


def get_weekday(timezone):
    # 返回当前周几
    timezone = pytz.timezone(timezone)
    now = datetime.now(timezone)
    # 字符串格式输出
    weekday = now.strftime("%A")
    return weekday


class time_tool:
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

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

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
NODE_CLASS_MAPPINGS = {"time_tool": time_tool}
NODE_DISPLAY_NAME_MAPPINGS = {"time_tool": "星期查询工具（weekday_tool）"}


if __name__ == "__main__":

    print(get_weekday("Asia/Shanghai"))
