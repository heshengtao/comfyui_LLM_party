import json
import locale
import os

import requests
from pydub import AudioSegment


def get_tenant_access_token(token_url, app_id, app_secret):
    token_data = {"app_id": app_id, "app_secret": app_secret}
    token_headers = {"Content-Type": "application/json"}
    token_response = requests.post(token_url, data=json.dumps(token_data), headers=token_headers)
    if token_response.status_code == 200:
        return token_response.json().get("tenant_access_token")
    else:
        print(token_response.text)
        raise Exception("Failed to get tenant_access_token")


class FeishuDownloadAudio:
    def __init__(self):
        self.tenant_access_token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        self.url_prefix = "https://open.feishu.cn/open-apis/im/v1/messages/"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "app_id": ("STRING", {}),
                "app_secret": ("STRING", {}),
                "message_id": ("STRING", {}),
                "file_key": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = ("audio_path", "show_help")

    FUNCTION = "download_audio"
    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def download_audio(self, app_id, app_secret, message_id, file_key, is_enable):
        show_help = "This function retrieves a file resource from a Feishu message."
        if not is_enable:
            return (
                None,
                show_help,
            )
        self.tenant_access_token = get_tenant_access_token(self.tenant_access_token_url, app_id, app_secret)

        headers = {"Authorization": f"Bearer {self.tenant_access_token}", "Content-Type": "application/json"}

        url = f"{self.url_prefix}{message_id}/resources/{file_key}?type=file"
        payload = ""
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            file_name = f"downloaded_file.opus"  # 你可能需要一个更好的方式来确定文件扩展名
            file_path = os.path.join(os.getcwd(), file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            wav_file_name = "converted_file.wav"
            wav_file_path = os.path.join(os.getcwd(), wav_file_name)

            # 使用pydub转换音频格式
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_file_path, format="wav")

            return (wav_file_path, show_help,)
        else:
            print("获取文件资源信息失败。")
            print("错误信息:", response.text)
            return (None, show_help,)


NODE_CLASS_MAPPINGS = {
    "FeishuDownloadAudio": FeishuDownloadAudio,
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
    NODE_DISPLAY_NAME_MAPPINGS = {"FeishuDownloadAudio": "飞书下载音频🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FeishuDownloadAudio": "Feishu Download Audio🐶"}


if __name__ == "__main__":
    obj = FeishuDownloadAudio()
    obj.download_audio(app_id="", app_secret="", message_id="", file_key="", is_enable=True)
