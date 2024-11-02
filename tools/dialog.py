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
                {"init_dialog": ("STRING", {}),
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

    def dialog(self, init_dialog,is_reload):
        if is_reload:
            self.start = True
        if self.start == False:
            # 读取prompt.txt文件内容
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        else:
            prompt = init_dialog
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

anything={}

class start_anything:
    def __init__(self):
        self.start = True

    @classmethod
    def INPUT_TYPES(s):
        global anything
        return {"required": 
                {"init_any": (any_type, {}),
                 "key": ("STRING", {"default":""}),
                 "is_reload": ("BOOLEAN", {"default": False})
                 }
                }

    RETURN_TYPES = (
        any_type,
    )
    RETURN_NAMES = (
        "any",
    )

    FUNCTION = "dialog"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, start_any, key,is_reload):
        if is_reload:
            self.start = True
        if self.start == False:
            global anything
            try:
                prompt= anything[key]
            except:
                prompt = start_any
                anything[key] = start_any
                self.start = False
        else:
            prompt = start_any
            anything[key] = start_any
            self.start = False
        return (
            prompt,
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
                "key": ("STRING", {"default":""}),
                "any": (any_type, {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "dialog"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def dialog(self, any,key):
        global anything
        anything[key] = any
        return ()