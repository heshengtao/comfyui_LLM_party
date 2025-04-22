import base64
import locale
import os
from datetime import datetime

import requests


class FileOnlineDelete_gitee:
    def __init__(self):
        self.url_prefix = "https://gitee.com/api/v5/repos/"
        self.show_help = "placeholder"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "repo_owner": ("STRING", {}),
                "repo_name": ("STRING", {}),
                "access_token": ("STRING", {}),
                "branch": ("STRING", {}),
                "file_path": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("show_help",)

    FUNCTION = "delete_file_from_branch"
    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def delete_file_from_branch(
        self, repo_owner, repo_name, file_path, branch, access_token, commit_message="[comfyui_LLM_party] file deleted"
    ):

        url = f"https://gitee.com/api/v5/repos/{repo_owner}/{repo_name}/contents/{file_path}"

        params = {"access_token": access_token, "ref": branch}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to get file info. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        file_sha = response.json()["sha"]

        data = {"access_token": access_token, "message": commit_message, "sha": file_sha, "branch": branch}
        response = requests.delete(url, json=data)

        if response.status_code == 200:
            print(f"File '{file_path}' successfully deleted from branch '{branch}'.")
            return ("Success",)
        else:
            print(f"Failed to delete file. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return (response.text,)


NODE_CLASS_MAPPINGS = {
    "FileOnlineDelete_gitee": FileOnlineDelete_gitee,
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
    NODE_DISPLAY_NAME_MAPPINGS = {"FileOnlineDelete_gitee": "清理Gitee文件床🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FileOnlineDelete_gitee": "Clean Gitee File Bed🐶"}


if __name__ == "__main__":
    file_path = "image.jpg"
    obj = FileOnlineDelete_gitee()
    obj.delete_file_from_branch(
        repo_owner="comfyui_LLM_party",
        repo_name="comfyui_LLM_party",
        branch="comfyui_LLM_party",
        file_path=file_path,
        access_token="comfyui_LLM_party",
    )
