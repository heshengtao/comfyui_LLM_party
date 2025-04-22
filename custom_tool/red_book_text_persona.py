import locale

class red_book_text_persona:
    @classmethod
    def INPUT_TYPES(s):
        text_type_list = ["产品文案", "活动文案"]
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "main_body": ("STRING", {"default": "Red Book Text Persona"}),
                "text_type": (text_type_list, {"default": "产品文案"}),
                "min_length": ("INT", {"default": 100}),
                "desc": ("STRING",{"default": ""} ),
            },
            "optional": {
                "must_include_tag": ("STRING",{"forceInput": True} ),
            },
        }
    
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("system_prompt_input","user_prompt_input",)

    FUNCTION = "red_book_text"

    CATEGORY = "大模型派对（llm_party）/面具（persona）"

    def red_book_text(self, main_body, text_type,min_length, desc,must_include_tag=None, is_enable=True):
        if is_enable == False:
            return (None,)
        if text_type == "产品文案":
            system_prompt = f"""# 产品文案助理

你是一位资深的小红书产品文案助理。

## 任务

请为产品“{main_body}”撰写一篇小红数风格的产品文案。产品的描述如下：
{desc}

## 要求

- 文案字数不少于{min_length}字
- 文案内容要有创意，吸引用户点击
- 可以适当的加入emoji、表情等元素
- 在文章的最后加上符合产品的标签（在小红书中标签的格式为#标签名,标签和标签之间用空格分开），标签应该在5个以上，10个以下
"""
            if must_include_tag is not None and must_include_tag != "":
                system_prompt += f"- 文案最后必须包含标签:{must_include_tag}\n"
            system_prompt += f"""

## 限制

直接输出文案即可，不要有多余的内容，或者重复需求。

接下来生成一篇产品“{main_body}”的小红书文案吧
"""
        elif text_type == "活动文案":
            system_prompt = f"""# 活动文案助理

你是一位资深的活动策划助理。

## 任务

请为活动“{main_body}”撰写一篇小红数风格的活动文案。活动的描述如下：
{desc}

## 要求

- 文案字数不少于{min_length}字
- 文案内容要有创意，吸引用户点击
- 可以适当的加入emoji、表情等元素
- 在文章的最后加上符合活动的标签（在小红书中标签的格式为#标签名，标签和标签之间用空格分开），标签应该在5个以上，10个以下
"""
            if must_include_tag is not None and must_include_tag != "":
                system_prompt += f"- 文案最后必须包含标签:{must_include_tag}\n"
            system_prompt += f"""


## 限制

直接输出文案即可，不要有多余的内容，或者重复需求。

接下来生成一篇活动“{main_body}”的小红书文案吧
"""
        return (system_prompt,main_body,)

NODE_CLASS_MAPPINGS = {
    "red_book_text_persona": red_book_text_persona,
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
    NODE_DISPLAY_NAME_MAPPINGS = {"red_book_text_persona": "小红书文案面具📕"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"red_book_text_persona": "REDnote copywriting Persona📕"}