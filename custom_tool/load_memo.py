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
        current_time = datetime.datetime.now()
        # 以时间戳作为ID，字符串格式 XX年XX月XX日XX时XX分XX秒并加上一个哈希值防止重复
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
        # 构建prompt.json的绝对路径，如果temp文件夹不存在就创建
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(current_dir_path, "temp"), exist_ok=True)
        self.prompt_path = os.path.join(current_dir_path, "temp", str(self.id) + ".json")
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(
                    [], f, indent=4, ensure_ascii=False
                )
        return {
            "required": {
                "historical_record": ("STRING", {"default":self.prompt_path}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "user_history",
        "history_path",
    )

    FUNCTION = "memo"

    # OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self, historical_record=""):
        if historical_record != "":
            temp_path = os.path.join(current_dir_path, "temp")
            self.prompt_path = os.path.join(temp_path, historical_record)      
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(
                    [], f, indent=4, ensure_ascii=False
                )
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            user_history=f.read()
        return (
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
    )
    RETURN_NAMES = (
    )

    FUNCTION = "memo"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self,history, history_path):
        # 最后两个元素
        history=json.loads(history)[-2:]
        with open(history_path, "r", encoding="utf-8") as f:
            old_history=json.load(f)
        old_history.extend(history)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(old_history, f, ensure_ascii=False)
        return ()

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

NODE_CLASS_MAPPINGS = {
    "load_memo": load_memo,
    "save_memo": save_memo,
}
lang = locale.getdefaultlocale()[0]



try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_memo": "加载记忆",
        "save_memo": "保存记忆",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_memo": "load memory",
        "save_memo": "save memory",
    }