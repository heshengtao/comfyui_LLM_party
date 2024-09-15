import hashlib
import json
import os
import datetime
import random

from ..config import config_path, current_dir_path, load_api_keys


class start_dialog:
    def __init__(self):
        self.start = True
        self.start_dialog=""
        current_time = datetime.datetime.now()
        # 生成一个hash值作为id
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
        # temp文件夹不存在就创建
        if not os.path.exists(os.path.join(current_dir_path, "temp")):
            os.makedirs(os.path.join(current_dir_path, "temp"))
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path, "temp", self.id + ".txt")
        # 如果文件不存在，创建prompt.txt文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                f.write("")

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                {"start_dialog": ("STRING", {}),
                 "is_reload": ("BOOLEAN", {"default": False})
                 }
                }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "user_prompt",
        "dialog_id",
    )

    FUNCTION = "dialog"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, start_dialog,is_reload):
        if is_reload:
            self.start = True
        if self.start == False:
            # 读取prompt.txt文件内容
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = start_dialog
            self.start = False
        dialog_id = self.id
        return (
            prompt,
            dialog_id,
        )
    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value

class end_dialog:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dialog_id": ("STRING", {"forceInput": True}),
                "assistant_response": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "dialog"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, dialog_id, assistant_response):
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path, "temp", dialog_id + ".txt")
        print(self.prompt_path)
        # 如果文件不存在，创建prompt.txt文件，存在就覆盖文件
        with open(self.prompt_path, 'w',encoding="utf-8") as file:
            file.write(assistant_response)
        return ()

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class start_anything:
    def __init__(self):
        self.start = True
        self.start_dialog=""
        current_time = datetime.datetime.now()
        # 生成一个hash值作为id
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
        # temp文件夹不存在就创建
        if not os.path.exists(os.path.join(current_dir_path, "temp")):
            os.makedirs(os.path.join(current_dir_path, "temp"))
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path, "temp", self.id + ".json")
        # 如果文件不存在，创建prompt.txt文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                f.write("")

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                {"start_any": (any_type, {}),
                 "key": ("STRING", {"default":""}),
                 "is_reload": ("BOOLEAN", {"default": False})
                 }
                }

    RETURN_TYPES = (
        any_type,
        "STRING",
    )
    RETURN_NAMES = (
        "any",
        "dialog_id",
    )

    FUNCTION = "dialog"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, start_any, key,is_reload):
        if is_reload:
            self.start = True
        if self.start == False:
            # 读取prompt.json中key的值
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt = json.load(f)
                prompt = prompt.get(key,"")
        else:
            prompt = start_any
            self.start = False
        dialog_id = self.id
        return (
            prompt,
            dialog_id,
        )
    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value

class end_anything:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dialog_id": ("STRING", {"forceInput": True}),
                "key": ("STRING", {"default":""}),
                "any": (any_type, {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "dialog"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, dialog_id, any,key):
        # 构建prompt.txt的绝对路径
        self.prompt_path = os.path.join(current_dir_path, "temp", dialog_id + ".json")
        print(self.prompt_path)
        # 如果文件不存在，创建prompt.json文件，存在就把any写入key的值
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump({key: any}, f, ensure_ascii=False, indent=4)
        else:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt = json.load(f)
                prompt[key] = any
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(prompt, f, ensure_ascii=False, indent=4)
        return ()