import json
import requests
from ..config import config_path, load_api_keys

api_keys = load_api_keys(config_path)
wechat_key=api_keys.get("wechat_key")
def send_wechat(content):
    global wechat_key
    webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={wechat_key}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    response = requests.post(webhook_url, headers=headers, json=data)

    print(response.text)

class work_wechat_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "key": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def web(self, is_enable=True,key=None):
        if is_enable == False:
            return (None,)
        
        global wechat_key
        if key is not None and key != "":
            wechat_key = key
        else:
            wechat_key = api_keys.get("wechat_key")
        output = [
            {
                "type": "function",
                "function": {
                    "name": "send_wechat",
                    "description": "向企业微信发送消息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "需要发送的消息，支持Markdown格式",
                            },
                        },
                        "required": ["content"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class work_wechat:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "key": ("STRING", {}),
                "content": ("STRING", {"default": "hello world"}),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "web"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def web(self, is_enable=True,key=None,content="hello world"):
        if is_enable == False:
            return (None,)
        
        global wechat_key
        if key is not None and key != "":
            wechat_key = key
        else:
            wechat_key = api_keys.get("wechat_key")
        send_wechat(content)
        return ()
