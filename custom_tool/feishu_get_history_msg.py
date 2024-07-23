import os
import json
import time
import requests
from dotenv import load_dotenv


def get_tenant_access_token(token_url, app_id, app_secret):
    token_data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    token_headers = {
        "Content-Type": "application/json"
    }
    token_response = requests.post(token_url, data=json.dumps(token_data), headers=token_headers)
    if token_response.status_code == 200:
        return token_response.json().get("tenant_access_token")
    else:
        print(token_response.text)
        raise Exception("Failed to get tenant_access_token")



class FeishuGetHistory:
    def __init__(self):
        load_dotenv()
        self.last_ts = 0
        self.url_msg = os.getenv("MESSAGE_URL")
        self.tenant_access_token_url = os.getenv("TENANT_ACCESS_TOKEN_URL")

        # self.app_id = os.getenv("APP_ID")
        # self.app_secret = os.getenv("APP_SECRET")
        # self.chat_type = os.getenv("CHAT_TYPE")
        # self.chat_id = os.getenv("CHAT_ID")

        # self.receive_id = os.getenv("CHAT_ID")
        # self.receive_id_type = "chat_id"
        
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "app_id": ("STRING", {}),
                "app_secret": ("STRING", {}),
                "chat_id": ("STRING", {}), # for group chat
                "mode": (["auto", "fixed_time_diff"], {"default": "fixed_time_diff"}),
                "time_diff_sec": ("INT", {"default": 60}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("response", "last_ts", "show_help",)

    FUNCTION = "get_history"

    CATEGORY = "大模型派对（llm_party）/函数（function）"


    def get_history(self,
                app_id=None,
                app_secret=None,
                chat_type=None,
                chat_id=None, # oc_xxx
                mode="auto",
                time_diff_sec=60): 
        show_help = "placeholder for help text"
        print(f"timestamp initialized to {self.last_ts}")
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

        self.tenant_access_token = get_tenant_access_token(self.tenant_access_token_url, self.app_id, self.app_secret)

        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            }

        end_time = int(time.time())
        if (mode == "auto"):
            if end_time - self.last_ts > 60:
                start_time = end_time - 60
            else:
                start_time = self.last_ts
        else:
            start_time = end_time - time_diff_sec
        params = {
            "receive_id_type": self.receive_id_type,
            "container_id_type": "chat",
            "container_id": self.receive_id,
            "sort_type": "ByCreateTimeAsc",
            "start_time": start_time,
            "end_time": end_time,
            "page_size": 10
        }

        response = requests.get(url=self.url_msg, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.text}")
            return (None, show_help,)

        while response.json().get("data").get("has_more") == True:
            params["page_token"] = response.json().get("data").get("page_token")
            response = requests.get(url=self.url_msg, headers=headers, params=params)
            print(response.json())
        tmp_last_ts = self.last_ts
        self.last_ts = end_time
        return (json.dumps(response.json()), str(tmp_last_ts), show_help,)

NODE_CLASS_MAPPINGS = {
    "FeishuGetHistory": FeishuGetHistory,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FeishuGetHistory": "飞书机器人读群历史🐶（FeishuGetHistory）",
}

if __name__ == "__main__":
    feishu = FeishuGetHistory()
    feishu.get_history(mode="auto")