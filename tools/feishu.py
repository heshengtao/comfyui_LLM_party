import json

import numpy as np
import requests
from PIL import Image
from requests_toolbelt import MultipartEncoder

from ..config import config_path, load_api_keys

# 输入pip install requests_toolbelt 安装依赖库
tenant_access_token = ""


def uploadImage(path):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {"image_type": "message", "image": (open(path, "rb"))}  # 需要替换具体的path
    multi_form = MultipartEncoder(form)
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers["Content-Type"] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers["X-Tt-Logid"])  # for debug or oncall
    print(response.content)  # Print Response
    # 返回图片的key
    return response.json()["data"]["image_key"]


api_keys = load_api_keys(config_path)
feishu_url = api_keys.get("feishu_url")
wake_word = ""


# 发送消息到飞书的函数
def send_feishu(content, msgtype="markdown"):
    global feishu_url, wake_word
    webhook_url = feishu_url
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if msgtype == "text":
        data = {
            "msg_type": msgtype,
            "content": {
                "text": wake_word + "\n" + content if wake_word != "" else content,
            },
        }
    elif msgtype == "image":
        data = {"msg_type": msgtype, "content": {"image_key": content}}

    # 发送POST请求到飞书服务器
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    # 返回响应状态码
    return response.status_code


class feishu_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
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

    def web(self, is_enable=True, url=None, key_word=""):
        if is_enable == False:
            return (None,)

        global feishu_url, wake_word
        if url is not None and url != "":
            feishu_url = url
        else:
            feishu_url = api_keys.get("feishu_url")

        if key_word is not None and key_word != "":
            wake_word = key_word

        output = [
            {
                "type": "function",
                "function": {
                    "name": "send_feishu",
                    "description": "向飞书发送消息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "需要发送的文字信息或者图片的key",
                            },
                            "msgtype": {
                                "type": "string",
                                "description": "消息类型，只支持text",
                                "default": "text",
                            },
                        },
                        "required": ["content", "msgtype"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class feishu:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "content": ("STRING", {"default": "hello world"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "msgtype": (["text", "image"], {"default": "text"}),
                "key_word": ("STRING", {"default": ""}),
            },
            "optional": {
                "image": ("IMAGE", {}),
                "url": ("STRING", {}),
                "feishu_app_id": ("STRING", {}),
                "feishu_app_secret": ("STRING", {}),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "web"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def web(
        self,
        image=None,
        is_enable=True,
        url=None,
        content="hello world",
        msgtype="text",
        key_word="",
        feishu_app_id="",
        feishu_app_secret="",
    ):
        if is_enable == False:
            return (None,)

        global feishu_url, wake_word
        if url is not None and url != "":
            feishu_url = url
        else:
            feishu_url = api_keys.get("feishu_url")

        if key_word is not None and key_word != "":
            wake_word = key_word

        if image is not None:
            # 请替换以下变量的值为您的应用凭证
            app_id = feishu_app_id
            app_secret = feishu_app_secret

            # 飞书API获取tenant_access_token的URL
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

            # 构建请求体
            payload = json.dumps({"app_id": app_id, "app_secret": app_secret})

            # 设置请求头
            headers = {"Content-Type": "application/json"}

            # 发送POST请求
            response = requests.post(url, headers=headers, data=payload)

            # 解析响应
            json_data = json.loads(response.text)

            # 打印返回体信息
            print(json_data)

            # 提取tenant_access_token
            if "code" in json_data and json_data["code"] == 0:
                global tenant_access_token
                tenant_access_token = json_data["tenant_access_token"]
            else:
                print("Failed to get Tenant Access Token")
            # 将张量转换为 NumPy 数组
            i = 255.0 * image[0].cpu().numpy()
            # 转换为图像并保存
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img.save("./output/feishu.png")
            image_key = uploadImage("./output/feishu.png")
            content = image_key

        send_feishu(content, msgtype)
        return ()
