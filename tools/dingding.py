import json

import requests

from ..config import config_path, load_api_keys

api_keys = load_api_keys(config_path)
dingding_url = api_keys.get("dingding_url")
wake_word = ""


# 发送消息到钉钉的函数
def send_dingding(content, msgtype="markdown"):
    global dingding_url, wake_word
    webhook_url = dingding_url
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if msgtype == "text":
        data = {
            "msgtype": msgtype,
            "text": {
                "content": wake_word + "\n" + content if wake_word != "" else content,
            },
        }
    elif msgtype == "markdown":
        data = {
            "msgtype": msgtype,
            "markdown": {"text": content, "title": wake_word},
        }

    # 发送POST请求到钉钉服务器
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    # 返回响应状态码
    return response.status_code


class Dingding_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "msgtype": (["text", "markdown"], {"default": "markdown"}),
                "key_word": ("STRING", {"default": ""}),
            },
            "optional": {
                "url": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"

    def web(self, is_enable=True, url=None, msgtype="markdown", key_word=""):
        if is_enable == False:
            return (None,)

        global dingding_url, wake_word
        if url is not None and url != "":
            dingding_url = url
        else:
            dingding_url = api_keys.get("dingding_url")

        if key_word is not None and key_word != "":
            wake_word = key_word
        output = [
            {
                "type": "function",
                "function": {
                    "name": "send_dingding",
                    "description": "向钉钉发送消息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "需要发送的消息，支持Markdown格式",
                            },
                            "msgtype": {
                                "type": "string",
                                "description": "消息类型，支持text、markdown",
                                "default": msgtype,
                            },
                        },
                        "required": ["content", "msgtype"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class Dingding:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "content": ("STRING", {"default": "hello world"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "msgtype": (["text", "markdown"], {"default": "markdown"}),
                "key_word": ("STRING", {"default": ""}),
            },
            "optional": {
                "url": ("STRING", {}),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "web"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def web(self, is_enable=True, url=None, content="hello world", msgtype="markdown", key_word=""):
        if is_enable == False:
            return (None,)

        global dingding_url, wake_word
        if url is not None and url != "":
            dingding_url = url
        else:
            dingding_url = api_keys.get("dingding_url")

        if key_word is not None and key_word != "":
            wake_word = key_word
        send_dingding(content, msgtype)
        return ()
