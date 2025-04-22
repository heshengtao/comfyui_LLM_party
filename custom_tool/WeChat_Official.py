import locale
import requests
import json

def create_draft(appid, secret, title, author, content):
    # 获取access_token的函数
    def get_access_token(appid, secret):
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
        response = requests.get(url)
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            raise Exception(f"Error getting access token: {data}")

    # 获取access_token
    access_token = get_access_token(appid, secret)

    # API URL
    url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'

    # 请求体数据
    data = {
        "articles": [
            {
                "title": title,
                "author": author,
                "content": content
            }
        ]
    }

    # 将数据转换为JSON格式
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

    # 发送POST请求
    response = requests.post(url, data=json_data)

    # 打印响应结果
    return response.json()

class send_to_wechat_official:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "appid": ("STRING", {"default": "appid"}),
                "secret": ("STRING", {"default": "secret"}),
                "title": ("STRING", {"default": "title"}),
                "author": ("STRING", {"default": "author"}),
                "content": ("STRING", {"default": "HTML content"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log",)

    FUNCTION = "time"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def time(self, appid, secret, title, author, content, is_enable=True):
        if is_enable == False:
            return (None,)
        try:
            result = create_draft(appid, secret, title, author, content)
            return (result,)
        except Exception as e:
            return (str(e),)
        


NODE_CLASS_MAPPINGS = {"send_to_wechat_official": send_to_wechat_official}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"send_to_wechat_official": "发送到微信公众号"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"send_to_wechat_official": "send to wechat official"}