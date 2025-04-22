import locale
import os
import json
import redis
import datetime
import hashlib
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)

class load_redis_memo:
    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "history_key": ("STRING", {"default": "1"}),
                "redis_host": ("STRING", {"default": "localhost"}),
                "redis_port": ("INT", {"default": 6379, "min": 1, "max": 65535}),
                "clear_memo": ("BOOLEAN", {"default": False}),
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
        "history_key",
    )

    FUNCTION = "memo"

    # OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self, system_prompt="", history_key="", redis_host="localhost", redis_port=6379, clear_memo=False):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

        if clear_memo:
            # 清空并重置为初始数据
            initial_data = json.dumps([{"role": "system", "content": system_prompt}], ensure_ascii=False, indent=4)
            self.redis_client.set(history_key, initial_data)
        elif not self.redis_client.exists(history_key):
            # 如果不存在，初始化一个包含系统提示的JSON字符串并存储到Redis中
            initial_data = json.dumps([{"role": "system", "content": system_prompt}], ensure_ascii=False, indent=4)
            self.redis_client.set(history_key, initial_data)
        
        user_history = self.redis_client.get(history_key).decode('utf-8')
        histories = json.loads(user_history)
        
        if system_prompt != "" and system_prompt is not None:
            for message in histories:
                if message["role"] == "system":
                    message["content"] = system_prompt
            updated_data = json.dumps(histories, ensure_ascii=False, indent=4)
            self.redis_client.set(history_key, updated_data)
        
        return (
            system_prompt,
            user_history,
            history_key,
        )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

class save_redis_memo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "history": ("STRING", {"forceInput": True}),
                "history_key": ("STRING", {"forceInput": True}),
                "redis_host": ("STRING", {"default": "localhost"}),
                "redis_port": ("INT", {"default": 6379, "min": 1, "max": 65535}),
            },
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "history_key",
    )

    FUNCTION = "memo"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/记忆（memory）"

    def memo(self, history, history_key, redis_host="localhost", redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

        new_history = json.loads(history)[1:]
        old_history = json.loads(self.redis_client.get(history_key).decode('utf-8'))
        old_history.extend(new_history)
        updated_data = json.dumps(old_history, ensure_ascii=False, indent=4)
        self.redis_client.set(history_key, updated_data)
        return (history_key,)

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value
    

NODE_CLASS_MAPPINGS = {
    "load_redis_memo": load_redis_memo,
    "save_redis_memo": save_redis_memo,
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
        "load_redis_memo": "加载redis记忆",
        "save_redis_memo": "保存redis记忆",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_redis_memo": "load redis memory",
        "save_redis_memo": "save redis memory",
    }