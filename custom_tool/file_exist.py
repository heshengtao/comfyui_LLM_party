import locale
import os

class FilePathExists:
    def __init__(self):
        self.exists = False

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("file_exists",)

    FUNCTION = "file_exists"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def file_exists(self, file_path=None, is_enable=True):
        if is_enable == False:
            return (self.exists)

        if self.exists == True:
            return (True,)

        if file_path == None:
            return (False,)

        if not isinstance(file_path, (str, bytes, os.PathLike)):
            print(f"Path is not a valid type: {type(file_path)}")
            return False

        self.exists = os.path.exists(file_path)
        return (self.exists,)

        

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
language = config.get("API_KEYS", "language")
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "FilePathExists": "路径已存在🐶"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "FilePathExists": "FilePathExists🐶"
    }