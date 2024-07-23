import os
import json
import requests
from requests_toolbelt import MultipartEncoder
from pydub import AudioSegment
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
        raise Exception("Failed to get tenant_access_token")



class FeishuSendMsg:
    def __init__(self):
        load_dotenv()
        self.url_img = os.getenv("IMAGE_UPLOAD_URL")
        self.url_file = os.getenv("FILE_UPLOAD_URL")
        self.url_msg = os.getenv("MESSAGE_URL")
        self.tenant_access_token_url = os.getenv("TENANT_ACCESS_TOKEN_URL")

        # self.app_id = os.getenv("APP_ID")
        # self.app_secret = os.getenv("APP_SECRET")
        # self.chat_type = os.getenv("CHAT_TYPE")
        # self.chat_type = os.getenv("CHAT_TYPE")
        # self.chat_id = os.getenv("CHAT_ID")
        # self.user_id = os.getenv("USER_ID")
        # self.open_id = os.getenv("OPEN_ID")

        # if (self.chat_type == "group"):
        #     self.receive_id = os.getenv("CHAT_ID")
        #     self.receive_id_type = "chat_id"
        # elif self.chat_type == "single":
        #     if self.user_id != "":
        #         self.receive_id = os.getenv("USER_ID")
        #         self.receive_id_type = "user_id"
        #     else:
        #         self.receive_id = os.getenv("OPEN_ID")
        #         self.receive_id_type = "open_id"
        
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "msg_type": (["text", "image", "audio"], {"default": "text"}),
                "text": ("STRING", {"default": "Hello. I am an AI from LLM_Party."}),
                "file_path": ("STRING", {"default": "image & audio file only"}),
                "app_id": ("STRING", {}),
                "app_secret": ("STRING", {}),
                "chat_type": (["group", "single"], {"default": "group"}),
                "chat_id": ("STRING", {}), # for group chat
                "user_id": ("STRING", {}), # for single chat
                "open_id": ("STRING", {}), # for single chat
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("file_key", "msg_id", "show_help")

    FUNCTION = "send_msg"

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def upload_image(self, image_path):
        form = {'image_type': 'message',
                'image': (open(image_path, 'rb'))} 
        multi_form = MultipartEncoder(form)
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": multi_form.content_type
        }
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.request("POST", self.url_img, headers=headers, data=multi_form)
        if response.status_code == 200:
            return response.json()['data']['image_key']
        else:
            raise Exception("Failed to upload image")

    def send_img(self, image_key):
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        params = {"receive_id_type": self.receive_id_type}
        post_data = {
            "receive_id": self.receive_id,
            "content": json.dumps({"image_key": image_key}),
            "msg_type": "image",
        }
        response = requests.post(self.url_msg, params=params, data=json.dumps(post_data), headers=headers)

        return response

    def upload_audio(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension.lower() != '.opus':
            audio = AudioSegment.from_file(file_path)
            opus_file_path = f"{file_name}.opus"
            audio.export(opus_file_path, format="opus")
            file_path = opus_file_path

        with open(file_path, 'rb') as file:
            file_name = os.path.basename(file_path)
            form = {
                'file_type': 'opus',
                'file_name': file_name,
                'duration': str(len(audio)),
                'file': file,
            }
            multi_form = MultipartEncoder(form)
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": multi_form.content_type
            }
            response = requests.request("POST", self.url_file, headers=headers, data=multi_form)

        if file_path != file_name + file_extension:
            os.remove(file_path)

        if response.status_code == 200:
            return response.json()['data']['file_key']
        else:
            print(response.text)
            raise Exception("Failed to upload file")

    def send_file(self, file_key):
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        params = {"receive_id_type": self.receive_id_type}
        post_data = {
            "receive_id": self.receive_id,
            "content": json.dumps({"file_key": file_key}),
            "msg_type": "audio",
        }
        response = requests.post(self.url_msg, params=params, data=json.dumps(post_data), headers=headers)
        return response


    def send_text(self, text):
        params = {"receive_id_type": self.receive_id_type}

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.tenant_access_token}"
        }

        msg_content = {
                "text": text,
            }

        post_data = {
            # https://open.feishu.cn/document/server-docs/group/chat/list?appId=cli_a612a3a341f9100b
            "receive_id": self.receive_id,  
            "msg_type": "text",  # 消息类型，这里以文本消息为例
            "content": json.dumps(msg_content),  # 消息内容
        }

        response = requests.post(self.url_msg, params=params, data=json.dumps(post_data), headers=headers)
        return response

    def send_msg(self,
                msg_type=None, 
                text=None, 
                file_path=None, 
                app_id=None,
                app_secret=None,
                chat_type=None,
                chat_id=None, # oc_xxx
                user_id=None,
                open_id=None,
                is_enable=True): # 6xxxx
        show_help = "placeholder for help text"
        if not is_enable:
            return (None, None, show_help,)
        if app_id is not None:
            self.app_id = app_id
        if app_secret is not None:
            self.app_secret = app_secret
        if chat_type is not None:
            self.chat_type = chat_type
        if chat_id is not None:
            self.chat_id = chat_id
        if user_id is not None:
            self.user_id = user_id
        if open_id is not None:
            self.open_id = open_id

        if self.chat_type == "group":
            self.receive_id_type = "chat_id"
            self.receive_id = self.chat_id
        elif self.chat_type == "single":
            if self.user_id != "":
                self.receive_id_type = "user_id"
                self.receive_id = self.user_id
            else:
                self.receive_id_type = "open_id"
                self.receive_id = self.open_id

        self.tenant_access_token = get_tenant_access_token(self.tenant_access_token_url, self.app_id, self.app_secret)

        if msg_type == "text":
            response = self.send_text(text)
            return (None, response.json().get("data").get("message_id"), show_help,)
        elif msg_type == "image":
            image_key = self.upload_image(file_path)
            response = self.send_img(image_key)
            return (image_key, response.json().get("data").get("message_id"), show_help,)
        elif msg_type == "audio":
            file_key = self.upload_audio(file_path)
            response = self.send_file(file_key)
            return (file_key, response.json().get("data").get("message_id"), show_help,)

NODE_CLASS_MAPPINGS = {
    "FeishuSendMsg": FeishuSendMsg,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FeishuSendMsg": "飞书机器人发消息🐶（FeishuSendMsg）",
}

if __name__ == "__main__":
    feishu = FeishuSendMsg()
    feishu.send_msg(msg_type="text", text="Hello. I am an AI from LLM Party.")
    feishu.send_msg(msg_type="image", file_path="D:\\aaaCode\\feishu\output\9c809373e1f617e1e2e3a5dc39adc0ed_8399068463954610687.jpg")
    feishu.send_msg(msg_type="audio", file_path="D:\\aaaCode\\feishu\output\\audio.wav")