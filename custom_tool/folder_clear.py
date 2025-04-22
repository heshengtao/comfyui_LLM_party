import os
import shutil
import locale
import configparser


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")


class FolderCleaner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any": (any_type, {}),
                "folder_path": ("STRING", {}),
                "file_type": (['image', 'audio', 'video', 'all_files', 'all'], {"default": 'image'}),
                "is_enable": ("BOOLEAN", {"default": True})
            }
        }
    
    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("any",)

    FUNCTION = "delete_files"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"
    
    def delete_files(self, any, folder_path, file_type='all', is_enable=True):
        if not is_enable:
            return (any,)

        file_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'audio': ['.mp3', '.wav', '.aac', '.flac'],
            'video': ['.mp4', '.avi', '.mov', '.mkv'],
            'all_files': ['.txt', '.pdf', '.docx', '.xlsx', 
                        '.mp4', '.avi', '.mov', '.mkv', 
                        '.mp3', '.wav', '.aac', '.flac', 
                        '.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'all': []  # all_files包括文件夹
        }

        if file_type in file_extensions:
            extensions = file_extensions[file_type]
        else:
            extensions = []

        for root, dirs, files in os.walk(folder_path):
            if root == folder_path:
                for file in files:
                    file_path = os.path.join(root, file)
                    _, ext = os.path.splitext(file)

                    if (file_type == 'all' or 
                        file_type == 'all_files' or 
                        (file_type != 'all_files' and ext in extensions)):
                        os.remove(file_path)

        if file_type != 'all':
            return (True,)

        for root, dirs, files in os.walk(folder_path):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)

        return (True,)
    

NODE_CLASS_MAPPINGS = {"FolderCleaner": FolderCleaner}

lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"FolderCleaner": "清空文件夹🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"FolderCleaner": "FolderCleaner🐶"}
