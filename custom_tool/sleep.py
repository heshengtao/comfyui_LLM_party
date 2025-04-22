import time
import locale
def interrupt_handler(signum, frame):
    print("Process interrupted")
    sys.exit(0)

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class time_sleep:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default":True}),
                "sleep_time": ("FLOAT", {"default": 0.5}),
                "any": (any_type, {}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("any",)

    FUNCTION = "sleep"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def sleep(self,sleep_time,any,is_enable=False):
        if is_enable == False:
            return (any,)
        else:
            time.sleep(sleep_time)
        return (any,)
        


NODE_CLASS_MAPPINGS = {"time_sleep": time_sleep}
# 获取系统语言
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
    NODE_DISPLAY_NAME_MAPPINGS = {"time_sleep": "延时模块"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"time_sleep": "delay module"}