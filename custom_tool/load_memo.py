import datetime
import hashlib
import json
import locale
import os
import random
import re
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)

class load_memo:
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "system_prompt": ("STRING", {"default": "","multiline": True}),
                "history_path": ("STRING", {"default":"1.json"}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "system_prompt",
        "user_history",
        "history_path",
    )

    FUNCTION = "memo"

    # OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self,system_prompt="", history_path=""):
        if history_path != "":
            temp_path = os.path.join(current_dir_path, "temp")
            self.prompt_path = os.path.join(temp_path, history_path)      
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(
                    [{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False
                )
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            user_history=f.read()
        histories = json.loads(user_history)
        if system_prompt != "" and system_prompt is not None:
            for message in histories:
                if message["role"] == "system":
                    message["content"] = system_prompt
        return (
            system_prompt,
            user_history,
            self.prompt_path,
        )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

class save_memo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "history": ("STRING", {"forceInput": True}),
                "history_path": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "history_path",
    )

    FUNCTION = "memo"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self,history, history_path):
        # 最后两个元素
        history=json.loads(history)[1:]
        with open(history_path, "r", encoding="utf-8") as f:
            old_history=json.load(f)
        old_history.extend(history)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(old_history, f, ensure_ascii=False, indent=4)
        return (history_path,)

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

NODE_CLASS_MAPPINGS = {
    "load_memo": load_memo,
    "save_memo": save_memo,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'



try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_memo": "加载json文件记忆",
        "save_memo": "保存json文件记忆",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_memo": "load json file memory",
        "save_memo": "save json file memory",
    }