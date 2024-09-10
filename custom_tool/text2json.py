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
        return {"required": {"text": ("STRING", {}), "sep": ("STRING", {"default": "\n"})}}

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("json_data",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/函数（function）"

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
        json_data = json.dumps(dict, ensure_ascii=False)
        return (json_data,)


import json


class text2parameters:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True})}}

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("json_data",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def convert_txt2json(self, text):
        # 统一成json的引号
        text = text.replace("'", '"')
        # 把json字符串转换为字典
        json_data = json.loads(text)
        return (json_data,)


NODE_CLASS_MAPPINGS = {"text2json": text2json, "text2parameters": text2parameters}
lang = locale.getdefaultlocale()[0]
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
if language == "zh_CN" or language == "en_US":
    lang = language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {"text2json": "文本分割成json🐶", "text2parameters": "文本转参数"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"text2json": "Split text into JSON🐶", "text2parameters": "Text to parameters"}


if __name__ == "__main__":
    text = f"""

在旧金山，你可以去金门公园，那里有免费的食物和饮料，以及各种户外设施。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去宪法大道，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。

在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去白宫，那里有免费的食物和饮料，以及各种户外设施。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。

在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去白宫，那里有免费的食物和饮料，以及各种户外设施。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。
在加州最幸福的事就是在午后的长椅上喝杯咖啡。
在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去白宫，那里有免费的食物和饮料，以及各种户外设施。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。


早上，没有人会打扰你。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。

在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去白宫，那里有免费的食物和饮料，以及各种户外设施。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。

在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

下午的时光是自由的。

在洛杉矶，你可以去好莱坞的星光大道，那里有免费的食物和饮料，以及各种户外设施。

在纽约，你可以去中央公园，那里有免费的食物和饮料，以及各种户外设施。

在波士顿，你可以去哈佛大学，那里有免费的食物和饮料，以及各种户外设施。

在芝加哥，你可以去南公园，那里有免费的食物和饮料，以及各种户外设施。

在华盛顿特区，你可以去白宫，那里有免费的食物和饮料，以及各种户外设施。"""
    out = text2json().convert_txt2json(text=text)
    print(out)
