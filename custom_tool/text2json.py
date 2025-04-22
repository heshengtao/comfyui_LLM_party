##########
# 将text按段落切分，转换为json格式
# 索引为0，1，2，...
##########
import codecs
import locale


def decode_escapes(text):
    return codecs.decode(text, "unicode_escape")


import json


class text2json:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), "sep": ("STRING", {"default": "\n"})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_data",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def convert_txt2json(self, text, sep="\n"):
        # 判断是不是转义
        if sep.startswith("\\"):
            sep = decode_escapes(sep)
        paragraphs = text.split(sep)
        idx = 0
        dict = {}
        for paragraph in paragraphs:
            if paragraph != "":
                dict[idx] = paragraph
                idx += 1
        json_data = json.dumps(dict, ensure_ascii=False, indent=4)
        return (json_data,)


import json

class text2parameters:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True})}}

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("json_data",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def convert_txt2json(self, text):
        # 统一成json的引号
        text = text.replace("'", '"')
        # 把json字符串转换为字典
        json_data = json.loads(text)
        return (json_data,)


NODE_CLASS_MAPPINGS = {"text2json": text2json,"text2parameters": text2parameters}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"text2json": "文本分割成json🐶", "text2parameters": "文本转参数"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"text2json": "Split text into JSON🐶", "text2parameters": "Text to parameters"}