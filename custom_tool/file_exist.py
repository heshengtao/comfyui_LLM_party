import locale
import os

class FilePathExists:
    def __init__(self):
        self.file_path = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = ("BOOLEAN","STRING",)
    RETURN_NAMES = ("file_exists","path_hold",)

    FUNCTION = "file_exists"
    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def file_exists(self, file_path="", is_enable=True):
        if is_enable:
            self.file_path = file_path
        if self.file_path == None or self.file_path=="":
            return (False,self.file_path,)
        if not isinstance(self.file_path, (str, bytes, os.PathLike)):
            print(f"Path is not a valid type: {type(self.file_path)}")
            return (False,self.file_path,)
        exists = os.path.exists(self.file_path)
        return (exists,self.file_path,)

        

NODE_CLASS_MAPPINGS = {
    "FilePathExists": FilePathExists,
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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "FilePathExists": "文件是否存在转布尔值🐶"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "FilePathExists": "FilePathExists To Bool🐶"
    }