import datetime
import hashlib
import json
import locale
import os
import time
import asyncio
import threading

import requests


def get_tenant_access_token(token_url, app_id, app_secret):
    token_data = {"app_id": app_id, "app_secret": app_secret}
    token_headers = {"Content-Type": "application/json"}
    token_response = requests.post(token_url, data=json.dumps(token_data), headers=token_headers)
    expire_time = time.time() + token_response.json().get('expire')
    if token_response.status_code == 200:
        return token_response.json().get("tenant_access_token"), expire_time
    else:
        print(token_response.text)
        raise Exception("Failed to get tenant_access_token")


class FeishuGetHistory:
    def __init__(self):
        self.last_ts = 0
        self.url_msg = "https://open.feishu.cn/open-apis/im/v1/messages"
        self.tenant_access_token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        self.auth_thread_started = False

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "app_id": ("STRING", {}),
                "app_secret": ("STRING", {}),
                "chat_id": ("STRING", {}),  # for group chat
                "mode": (["auto", "fixed_time_diff"], {"default": "auto"}),
                "time_diff_sec": ("INT", {"default": 60}),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "BOOLEAN",
        "BOOLEAN",
        "BOOLEAN",
        "STRING",
    )
    RETURN_NAMES = (
        "response",
        "log_info",
        "message_id",
        "output_is_text",
        "output_is_audio",
        "output_is_image",
        "show_help",
    )

    FUNCTION = "get_history"

    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    async def refresh_auth(self):
        while True:
            if time.time() >= self.expire_time - 1800:
                self.tenant_access_token, self.expire_time = get_tenant_access_token(self.tenant_access_token_url, self.app_id, self.app_secret)
                print(f'auth token refreshed, expired at {self.expire_time}, now: {time.time()}, duration: {self.expire_time - time.time()}')
            await asyncio.sleep(1)

    def get_history(
        self, app_id=None, app_secret=None, chat_type=None, chat_id=None, mode="auto", time_diff_sec=60  # oc_xxx
    ):
        show_help = "placeholder for help text"
        if app_id is not None:
            self.app_id = app_id
        if app_secret is not None:
            self.app_secret = app_secret
        if chat_type is not None:
            self.chat_type = chat_type
        if chat_id is not None:
            self.chat_id = chat_id

        self.receive_id_type = "chat_id"
        self.receive_id = self.chat_id

        self.tenant_access_token, self.expire_time = get_tenant_access_token(self.tenant_access_token_url, self.app_id, self.app_secret)
        print(f'auth token init, expired at {self.expire_time}, now: {time.time()}, duration: {self.expire_time - time.time()}')

        # if not self.auth_thread_started:
        #     threading.Thread(target=lambda: asyncio.run(self.refresh_auth()), daemon=True).start()
        #     self.auth_thread_started = True

        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
        }

        end_time = int(time.time())
        if mode == "fixed_time_diff":
            start_time = end_time - time_diff_sec
            params = {
                "receive_id_type": self.receive_id_type,
                "container_id_type": "chat",
                "container_id": self.receive_id,
                "sort_type": "ByCreateTimeAsc",
                "start_time": start_time,
                "end_time": end_time,
                "page_size": 50,
            }
            response = requests.get(url=self.url_msg, headers=headers, params=params)

        elif mode == "auto":
            setup_time = int(time.time())
            start_time = int(time.time())
            end_time = int(time.time())
            while True:
                params = {
                    "receive_id_type": self.receive_id_type,
                    "container_id_type": "chat",
                    "container_id": self.receive_id,
                    "sort_type": "ByCreateTimeAsc",
                    "start_time": start_time,
                    "end_time": end_time,
                    "page_size": 50,
                }
                response = requests.get(url=self.url_msg, headers=headers, params=params)
                if response.status_code != 200:
                    print(f"Error: {response.text}")
                    return (
                        None,
                        response.text,
                        None,
                        False,
                        False,
                        False,
                        show_help,
                    )
                items = response.json().get("data").get("items")
                if setup_time - start_time > 60 *30:
                    self.tenant_access_token = get_tenant_access_token(self.tenant_access_token_url, self.app_id, self.app_secret)
                    setup_time= int(time.time())
                if items:
                    if response.json()["data"]["items"][0]["sender"]["sender_type"] == "user":
                        break
                    else:
                        start_time = end_time
                        end_time = int(time.time())
                    # while response.json().get("data").get("has_more") == True:
                    #     params["page_token"] = response.json().get("data").get("page_token")
                    #     response = requests.get(url=self.url_msg, headers=headers, params=params)
                elif response.status_code != 200:
                    break
                else:
                    time.sleep(2)
                    start_time = end_time
                    end_time = int(time.time())

        if response.status_code != 200:
            print(f"Error: {response.text}")
            return (
                None,
                response.text,
                None,
                False,
                False,
                False,
                show_help,
            )

        msg = response.json()["data"]["items"][0]
        msg_type = msg["msg_type"]
        msg_id = msg["message_id"]
        msg_content = msg["body"]["content"]
        flag_audio = False
        flag_text = False
        flag_image = False
        if msg_type == "audio":
            flag_audio = True
        elif msg_type == "text":
            flag_text = True
        elif msg_type == "image":
            flag_image = True
        elif msg_type == "post":
            msg_content = json.loads(msg_content)
            msg_list = msg_content["content"]
            msg_content = {}
            for msg in msg_list:
                if msg[0]["tag"] == "text":
                    # 添加text元素到msg_content
                    msg_content["text"] = msg[0]["text"]
                    flag_text = True
                    print(msg_content)
                elif msg[0]["tag"] == "img":
                    msg_content["image_key"] = msg[0]["image_key"]
                    flag_image = True
                    print(msg_content)
                elif msg[0]["tag"] == "audio":
                    msg_content["file_key"] = msg[0]["file_key"]
                    flag_audio = True
            msg_content = json.dumps(msg_content, ensure_ascii=False)
        return (
            msg_content,
            json.dumps(response.json(), indent=4, ensure_ascii=False),
            msg_id,
            flag_text,
            flag_audio,
            flag_image,
            show_help,
        )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


NODE_CLASS_MAPPINGS = {
    "FeishuGetHistory": FeishuGetHistory,
}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"FeishuGetHistory": "飞书机器人读群历史🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FeishuGetHistory": "Feishu Bot Read Group History🐶"}

if __name__ == "__main__":
    feishu = FeishuGetHistory()
    feishu.get_history(mode="auto")
