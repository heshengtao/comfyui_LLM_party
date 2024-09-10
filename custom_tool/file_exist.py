import locale
import os


class FilePathExists:
    def __init__(self):
        self.file_path = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"file_path": ("STRING", {}), "is_enable": ("BOOLEAN", {"default": True})}}

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("file_exists",)

    FUNCTION = "file_exists"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def file_exists(self, file_path="", is_enable=True):
        if is_enable:
            self.file_path = file_path
        if self.file_path == None or self.file_path == "":
            return (False,)
        if not isinstance(self.file_path, (str, bytes, os.PathLike)):
            print(f"Path is not a valid type: {type(self.file_path)}")
            return (False,)
        exists = os.path.exists(self.file_path)
        return (exists,)


NODE_CLASS_MAPPINGS = {
    "FilePathExists": FilePathExists,
}
lang = locale.getdefaultlocale()[0]
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
if language == "zh_CN" or language == "en_US":
    lang = language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"FilePathExists": "路径已存在🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FilePathExists": "FilePathExists🐶"}
