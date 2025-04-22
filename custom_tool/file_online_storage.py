import base64
import locale
import os
from datetime import datetime

import requests


class FileOnlineStorage_gitee:
    def __init__(self):
        self.branch = "master"
        self.url_prefix = "https://gitee.com/api/v5/repos/"
        self.show_help = "1. 确保Gitee账号有创建仓库和上传文件的权限 2. target_branch为空时默认创建新分支 3. 相同分支下不能有重名文件"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "repo_owner": ("STRING", {}),
                "repo_name": ("STRING", {}),
                "access_token": ("STRING", {}),
                "target_branch": ("STRING", {}),
                "file_path": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("download_url", "branch_name", "file_name", "show_help")

    FUNCTION = "upload_file"
    CATEGORY = "大模型派对（llm_party）/APP链接（app link）"

    def check_repo_initialized(self):
        url = f"{self.url_prefix}{self.repo_owner}/{self.repo_name}/branches"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        return len(response.json()) > 0

    def initialize_repo(self):
        url = f"{self.url_prefix}{self.repo_owner}/{self.repo_name}/contents/README.md"
        data = {
            "access_token": self.access_token,
            "content": base64.b64encode(b"# [comfyui_LLM_party] first commit").decode("utf-8"),
            "message": "[comfyui_LLM_party] first commit",
        }
        response = requests.post(url, json=data)
        return response.status_code == 201

    def check_branch_exists(self):
        url = f"{self.url_prefix}{self.repo_owner}/{self.repo_name}/branches/{self.target_branch}"
        params = {"access_token": self.access_token}
        response = requests.get(url, params=params)
        return response.status_code == 200

    def create_new_branch(self, new_branch_name=None, base_branch=None):
        url = f"{self.url_prefix}{self.repo_owner}/{self.repo_name}/branches"

        if new_branch_name is None:
            new_branch_name = f"upload-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        if base_branch is None:
            base_branch = self.branch

        data = {"access_token": self.access_token, "branch_name": new_branch_name, "refs": base_branch}

        response = requests.post(url, data=data)

        if response.status_code == 201:
            print(f"New branch created: {new_branch_name}")
            self.branch_name = new_branch_name
        else:
            print(f"Failed to create new branch. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            self.branch_name = None

        return self.branch_name

    def upload_file(self, repo_owner, repo_name, file_path, access_token, target_branch=None):

        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.access_token = access_token
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.target_branch = target_branch

        if not self.check_repo_initialized():
            print("Repository is not initialized. Initializing...")
            if not self.initialize_repo():
                print("Failed to initialize repository")
                return (
                    None,
                    None,
                    None,
                    self.show_help,
                )

        if self.target_branch is not None:
            if not self.check_branch_exists():
                self.create_new_branch(new_branch_name=target_branch)
            else:
                self.branch_name = self.target_branch
        else:
            self.create_new_branch()

        if not self.branch_name:
            print("Failed to create new branch")
            return (
                None,
                None,
                None,
                self.show_help,
            )

        url = f"{self.url_prefix}{repo_owner}/{repo_name}/contents/{self.file_name}"
        with open(self.file_path, "rb") as file:
            content = file.read()
        content_base64 = base64.b64encode(content).decode("utf-8")
        data = {
            "access_token": self.access_token,
            "content": content_base64,
            "message": f"Upload file {self.file_name} via API",
            "branch": self.branch_name,
            "path": self.file_name,
        }
        response = requests.post(url, json=data)

        if response.status_code == 201:
            result = response.json()
            self.download_url = result["content"]["download_url"]
        else:
            print(f"Upload failed. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            self.download_url = None
        return (
            self.download_url,
            self.branch_name,
            self.file_name,
            self.show_help,
        )


NODE_CLASS_MAPPINGS = {
    "FileOnlineStorage_gitee": FileOnlineStorage_gitee,
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
    NODE_DISPLAY_NAME_MAPPINGS = {"FileOnlineStorage_gitee": "上传Gitee文件床🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FileOnlineStorage_gitee": "Upload to Gitee File Bed🐶"}


if __name__ == "__main__":
    obj = FileOnlineStorage_gitee()
    obj.upload_file(
        repo_owner="comfyui_LLM_party",
        repo_name="comfyui_LLM_party",
        file_path="comfyui_LLM_party",
        access_token="comfyui_LLM_party",
        target_branch="comfyui_LLM_party",
    )
    print(obj.download_url)
