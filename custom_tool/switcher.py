import locale
class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class any_switcher:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "num": ("INT", {"min": 1, "max": 10, "step": 1,"default":1}),
            },
            "optional": {
                "any1": (any_type, {}),
                "any2": (any_type, {}),
                "any3": (any_type, {}),
                "any4": (any_type, {}),
                "any5": (any_type, {}),
                "any6": (any_type, {}),
                "any7": (any_type, {}),
                "any8": (any_type, {}),
                "any9": (any_type, {}),
                "any10": (any_type, {})
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("which_any",)

    FUNCTION = "url_to_img"
    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def url_to_img(self, any1=None, any2=None, any3=None, any4=None, any5=None, any6=None, any7=None, any8=None, any9=None, any10=None, num=1):
        kwarg = locals()["any{}".format(num)]
        if kwarg is None:
            return (None,)
        else:
            return (kwarg,)

NODE_CLASS_MAPPINGS = {
    "any_switcher": any_switcher,
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
        "any_switcher": "任意类型切换器"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "any_switcher": "Any Type Switcher"
    }