import configparser
import io
import json
import locale
import os
import time
import cv2
import requests
from PIL import Image
import numpy as np
import openai
from openai import AzureOpenAI
import base64
from langchain_text_splitters import RecursiveCharacterTextSplitter
import torch
import easyocr
# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
config_key = configparser.ConfigParser()
config_key.read(config_path, encoding="utf-8")
class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")
def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


class mini_party:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "prompt": ("STRING", {"default": "input function here","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        prompt,
        model_name,
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        history= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_str}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output = response.choices[0].message.content
        return (output,)
    

class mini_translate:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "target_language": ("STRING", {"default": "English"}),
                "tone": ("STRING", {"default": "正式"}),
                "degree": ("INT", {"default": 5, " min": 0, "max": 10}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        target_language, 
        degree=5, 
        tone="正式",
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f"""你是一个翻译专家，请将我的输入翻译成{target_language}，语气为{tone}，语气程度为{str(degree)}。
语气程度最大为10，最小为0，数字越大语气越{tone}。当语气程度为0时，几乎不改变原文的语气，当语气程度为10时，语气会非常{tone}。
即使我的输入的语言和{target_language}相同，也请注意语气的调整，而不是返回原内容。
翻译时不要复述原文以及其他无关内容，直接返回翻译后的内容即可。注意！如果我输入的内容带有格式（例如markdown格式），请保留原格式。

如果是markdown格式的文字，有以下要求：
1. 请保留原格式，不要改变markdown格式。
2. 请不要改变markdown格式中的超链接中的()部分，但[]中的内容必须翻译。如果改变了()部分，可能会导致超链接失效。
3. HTML格式的文字，请保留原格式，不要改变HTML格式,其中会被显示在前端的文字需要翻译，而链接部分不能翻译。

从现在开始，请将以下内容翻译成{target_language}。
        """

        # 将file_content用RecursiveCharacterTextSplitter分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=0
        )
        output=""
        for chunk in text_splitter.split_text(input_str):   
            history= [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": chunk}
            ]
            openai_client = openai
            if "openai.azure.com" in openai.base_url:
                # 获取API版本
                api_version = openai.base_url.split("=")[-1].split("/")[0]
                # 获取azure_endpoint
                azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
                azure = AzureOpenAI(
                    api_key= openai.api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint,
                )
                openai_client = azure
            response = openai_client.chat.completions.create(
                                model=model_name,
                                messages=history,
                            )
            output += response.choices[0].message.content
            time.sleep(0.5)
        return (output,)

class mini_error_correction:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("input_text","output_text","error",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f"""你是一个文档纠错大师，你会纠正我输入的文字中的包括但不限于错别字、语法错误、病句、拼写错误等一系列文档错误，并给出修改后的内容以及错误的位置。
输出格式为json，格式如下：
{{
    "input_str": "输入的文字，用** **将错误的地方括起来",
    "output_str": "修改后的文字，保留原格式。",
    "error":"你修改的部分，如果没有错误则为空字符串。如果有错误，则用无序列表的形式列出错误"
}}

示例：
{{
    "input_str": "三年中，这个县的粮食产量以平均每年递增20%的速度大踏步地**向前发展**。他主动为这个系工程力学专业的两届船舶结构力学学习班**挑起**了薄壳力学、船舶结构力学等课程的主讲任务。",
    "output_str": "三年中，这个县的粮食产量以平均每年递增20%的速度大踏步地提高。他主动为这个系工程力学专业的两届船舶结构力学学习班承担了薄壳力学、船舶结构力学等课程的主讲任务。",
    "error":"- 向前发展 -> 提高\n- 挑起 -> 承担\n"
}}

从现在开始，请对我的输入进行纠错。注意！input_str里要用** **将错误的地方括起来；output_str里要保留原格式，不用加** **括起来；如果有错误，则用无序列表的形式列出错误。
        """

        # 将file_content用RecursiveCharacterTextSplitter分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=0
        )
        input_text=""
        output_text=""
        error=""
        for chunk in text_splitter.split_text(input_str):   
            history= [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": chunk}
            ]
            openai_client = openai
            if "openai.azure.com" in openai.base_url:
                # 获取API版本
                api_version = openai.base_url.split("=")[-1].split("/")[0]
                # 获取azure_endpoint
                azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
                azure = AzureOpenAI(
                    api_key= openai.api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint,
                )
                openai_client = azure
            response = openai_client.chat.completions.create(
                                model=model_name,
                                messages=history,
                                response_format={"type": "json_object"},
                            )
            output = response.choices[0].message.content
            output = json.loads(output)
            input_text += output["input_str"]
            output_text += output["output_str"]
            error += output["error"] + "\n"
            time.sleep(0.5)
        return (input_text,output_text,error,)


class mini_summary:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f"""你是一个文档总结助手，请根据我给出的文字，进行总结。
总结时，你需要抓住文中的要点，不要重复也不要遗漏，尽可能的把文中重要的、有价值的、新颖的、有趣的地方体现在总结中，并按照以下格式输出：

- 要点：xxxx
- 要点：xxxx
- 要点：xxxx

请严格按照以上格式输出，不要输出其他内容。
        """

        # 将file_content用RecursiveCharacterTextSplitter分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=400
        )
        output_text=""
        for chunk in text_splitter.split_text(input_str):   
            history= [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": chunk}
            ]
            openai_client = openai
            if "openai.azure.com" in openai.base_url:
                # 获取API版本
                api_version = openai.base_url.split("=")[-1].split("/")[0]
                # 获取azure_endpoint
                azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
                azure = AzureOpenAI(
                    api_key= openai.api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint,
                )
                openai_client = azure
            response = openai_client.chat.completions.create(
                                model=model_name,
                                messages=history,
                            )
            output = response.choices[0].message.content
            output_text += output+"\n"
            time.sleep(0.5)
        sys_prompt2 = f"""你是一个文档总结助手，我将给你一个已经总结过的要点报告，请根据我给出的要点报告，进行总结。
总结时，先阐述全文的主题，再阐述各部分的主旨，最后再对结论进行总结。采用总分总的形式进行总结。
"""
        history= [
            {"role": "system", "content": sys_prompt2},
            {"role": "user", "content": output_text}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )      
        output2 = response.choices[0].message.content
        return (output2,)

class mini_story:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "theme": ("STRING", {"default": "龟兔赛跑的故事","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("story","character",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        theme,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f"""你是一个故事设计大师，根据我接下来给出的主题，生成一个剧情完整的故事，并且给出故事中每一个角色的外观描述词。
输出格式为json，格式如下：

{{
    "story": "根据我接下来给出的主题，生成的一个剧情完整故事，和我输入的主题相关，且和我输入主题使用的语言一致。",
    "character": {{
        "角色1": "角色1的外观描述词，必须用英文描述",
        "角色2": "角色2的外观描述词，必须用英文描述"
    }},
}}

示例（例如我给出的主题是龟兔赛跑的故事）：

{{
    "story": "从前，在一个美丽的森林里，住着许多可爱的动物。其中有一只骄傲的兔子和一只勤奋的乌龟。兔子有一身雪白的毛发，长长的耳朵总是竖得高高的，眼睛像两颗红宝石，闪闪发光。它跑得非常快，总是喜欢在森林里炫耀自己的速度。乌龟则有着坚硬的绿色壳子，壳上布满了深浅不一的纹路。它的四肢短而有力，虽然行动缓慢，但每一步都走得很稳重。乌龟的眼睛小而明亮，透露出一股坚定的神情。一天，兔子在森林里遇到了乌龟，嘲笑它走得太慢。兔子说：“乌龟，你走得这么慢，连比赛都不敢参加吧？”乌龟不甘示弱，回答道：“兔子，我们来比赛跑步吧，我相信我能赢你。”兔子听了哈哈大笑，觉得这简直是天大的笑话，但它还是答应了比赛。比赛的消息很快传遍了整个森林，所有的动物都来围观。比赛开始了，兔子像箭一样冲了出去，很快就把乌龟远远地甩在了后面。跑了一段路后，兔子回头一看，发现乌龟还在远处慢慢地爬着。兔子心想：“乌龟这么慢，我还是先休息一下吧。”于是，它在路边找了个阴凉的地方，躺下睡着了。乌龟一步一步地向前爬着，虽然很慢，但它从未停下。它心里想着：“只要我不停下来，总会到达终点的。”就这样，乌龟坚持不懈地向前爬，终于超过了还在睡觉的兔子。当兔子醒来时，发现乌龟已经快到终点了。兔子急忙起身，拼命地向终点跑去，但已经太晚了。乌龟稳稳地爬过了终点线，赢得了比赛。森林里的动物们都为乌龟欢呼，兔子则羞愧地低下了头。乌龟对兔子说：“兔子，骄傲自满是不会带来胜利的，只有坚持不懈，才能取得成功。”从那以后，兔子不再骄傲自满，乌龟也继续保持着它的勤奋和坚持。森林里的动物们都从这场比赛中学到了宝贵的教训，大家和睦相处，过着幸福的生活。",
    "character": {{
        "兔子": "A rabbit with snow-white hair, long ears, and ruby eyes.",
        "乌龟": "A turtle with a hard green shell, shades of stripes, short, powerful limbs, and small, bright eyes"
    }}
}}

从现在开始，请对我的输入的主题开始撰写故事和人物外观描述。
        """
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": theme}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"},
                        )
        output = response.choices[0].message.content
        output= json.loads(output)
        story = output["story"]
        character = output["character"]
        character= json.dumps(character, ensure_ascii=False, indent=4)
        return (story,character,)

class mini_ocr:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "gpu": ("BOOLEAN", {"default": True,}),
                "language_name": ("STRING", {"default": "ch_sim,en"}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "imgbb_api_key":(
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING",)
    RETURN_NAMES = ("images", "masks", "json_str","text",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def OCR(self, 
            image, 
            gpu, 
            language_name, 
            ):
        out_images = []
        out_masks = []
        out_json = []
        out_text = []


        for item in image:
            image_pil = Image.fromarray(np.clip(255.0 * item.cpu().numpy(), 0, 255).astype(np.uint8)).convert("RGB")

            languages = language_name.split(",")
            reader = easyocr.Reader(languages, gpu=gpu)
            result = reader.readtext(np.array(image_pil), detail=1)
            result_text = reader.readtext(np.array(image_pil), detail=0)
            
            W, H = image_pil.size
            mask = np.zeros((H, W, 1), dtype=np.uint8)
            image_with_boxes = np.array(image_pil)

            parsed_result = []
            for (bbox, text, prob) in result:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))

                cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 0, 255), 2)
                cv2.putText(image_with_boxes, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)

                parsed_result.append({
                    "bounding_box": {
                        "top_left": [int(coord) for coord in bbox[0]],
                        "top_right": [int(coord) for coord in bbox[1]],
                        "bottom_right": [int(coord) for coord in bbox[2]],
                        "bottom_left": [int(coord) for coord in bbox[3]]
                    },
                    "text": text,
                    "confidence": float(prob)
                })

            out_images.append(torch.from_numpy(image_with_boxes.astype(np.float32) / 255.0).unsqueeze(0))
            out_masks.append(torch.from_numpy(mask.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0))
            out_json.append(parsed_result)
            out_text.append(result_text)

        json_result = json.dumps(out_json, ensure_ascii=False, indent=4)
        return torch.cat(out_images, dim=0), torch.cat(out_masks, dim=0), json_result

    def file(
        self,
        image, 
        gpu, 
        language_name, 
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        imgbb_api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f"""你是一个图片文字识别工具。请根据输入的图片以及我用OCR工具扫描后的json结果，综合识别出图片中的文字，并输出文字的坐标和内容。
输出时，请使用和我输入的json格式保持一致。注意，我给出的是OCR扫描的结果，并不准确，你需要根据图片内容进行判断和修正文字部分，坐标部分无需修改。
        
从现在开始，请对我的输入的图片进行提取文字。
        """

        out_images, out_masks, out_json = self.OCR(image, gpu, language_name)
        if imgbb_api_key == "" or imgbb_api_key is None:
            imgbb_api_key = api_keys.get("imgbb_api")
        if imgbb_api_key == "" or imgbb_api_key is None:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_json = [
                {"type": "text", "text": out_json},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_str}"},
                },
            ]
        else:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_api_key, "image": img_str}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
                print(img_url)
            else:
                return "Error: " + response.text
            img_json = [
                {"type": "text", "text": out_json},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ]
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": img_json}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"},
                        )
        output = response.choices[0].message.content
        history= [
            {"role": "system", "content": "将这个包含文字坐标信息的json转化成markdown格式，请参照json中的文字位置坐标，安排好markdown中的文字位置，并输出markdown格式的文本。"},
            {"role": "user", "content": output}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response2 = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output_text = response2.choices[0].message.content
        return (out_images, out_masks,output,output_text,)

class mini_sd_prompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "a girl","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "seed": ("INT", {"default": 42,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("positive_prompt","negative_prompt",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        prompt,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        seed=42,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f'''# Stable Diffusion prompt 助理

你来充当一位有艺术气息的Stable Diffusion prompt 助理。

## 任务

我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后转化成一份详细的、高质量的prompt，让Stable Diffusion可以生成高质量的图像。

## 背景介绍

Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。

## prompt 概念

- 完整的prompt包含“**Positive Prompt:**”和"**Negative Prompt:**"两部分。
- Positive prompt 用来描述图像，由普通常见的单词构成，使用英文半角","做为分隔符。
- negative prompt用来描述你不想在生成的图像中出现的内容。
- 以","分隔的每个单词或词组称为 tag。所以prompt和negative prompt是由系列由","分隔的tag组成的。

## () 和 [] 语法

调整关键字强度的等效方法是使用 () 和 []。 (keyword) 将tag的强度增加 1.1 倍，与 (keyword:1.1) 相同，最多可加三层。 [keyword] 将强度降低 0.9 倍，与 (keyword:0.9) 相同。

## Prompt 格式要求

你需要用以下json格式输出：
{{
"positive":"",
"negative":""
}}

下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节。

### 1. positive prompt 要求

- 你输出的 Stable Diffusion prompt 放入json字典的"positive"对应的值中。
- Positive prompt 内容包含画面主体、材质、附加细节、图像质量、艺术风格、色彩色调、灯光等部分，但你输出的 prompt 不能分段，例如类似"medium:"这样的分段描述是不需要的，也不能包含":"和"."。
- 画面主体：不简短的英文描述画面主体, 如 A girl in a garden，主体细节概括（主体可以是人、事、物、景）画面核心内容。这部分根据我每次给你的主题来生成。你可以添加更多主题相关的合理的细节。
- 对于人物主题，你必须描述人物的眼睛、鼻子、嘴唇，例如'beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,longeyelashes'，以免Stable Diffusion随机生成变形的面部五官，这点非常重要。你还可以描述人物的外表、情绪、衣服、姿势、视角、动作、背景等。人物属性中，1girl表示一个女孩，2girls表示两个女孩。
- 材质：用来制作艺术品的材料。 例如：插图、油画、3D 渲染和摄影。 Medium 有很强的效果，因为一个关键字就可以极大地改变风格。
- 附加细节：画面场景细节，或人物细节，描述画面细节内容，让图像看起来更充实和合理。这部分是可选的，要注意画面的整体和谐，不能与主题冲突。
- 图像质量：这部分内容开头永远要加上“(best quality,4k,8k,highres,masterpiece:1.2),ultra-detailed,(realistic,photorealistic,photo-realistic:1.37)”， 这是高质量的标志。其它常用的提高质量的tag还有，你可以根据主题的需求添加：HDR,UHD,studio lighting,ultra-fine painting,sharp focus,physically-based rendering,extreme detail description,professional,vivid colors,bokeh。
- 艺术风格：这部分描述图像的风格。加入恰当的艺术风格，能提升生成的图像效果。常用的艺术风格例如：portraits,landscape,horror,anime,sci-fi,photography,concept artists等。
- 色彩色调：颜色，通过添加颜色来控制画面的整体颜色。
- 灯光：整体画面的光线效果。

### 2. negative prompt 要求
- negative prompt部分放入json字典的"negative"对应的值中。你想要避免出现在图像中的内容都可以添加到"**Negative Prompt:**"后面。
- 任何情况下，negative prompt都要包含这段内容："nsfw,(low quality,normal quality,worst quality,jpeg artifacts),cropped,monochrome,lowres,low saturation,((watermark)),(white letters)"
- 如果是人物相关的主题，你的输出需要另加一段人物相关的 negative prompt，内容为：“skin spots,acnes,skin blemishes,age spot,mutated hands,mutated fingers,deformed,bad anatomy,disfigured,poorly drawn face,extra limb,ugly,poorly drawn hands,missing limb,floating limbs,disconnected limbs,out of focus,long neck,long body,extra fingers,fewer fingers,,(multi nipples),bad hands,signature,username,bad feet,blurry,bad body”。

### 3. 限制：
- tag 内容用英语单词或短语来描述，并不局限于我给你的单词。注意只能包含关键词或词组。
- 注意不要输出句子，不要有任何解释。
- tag数量限制40个以内，单词数量限制在60个以内。
- tag不要带引号("")。
- 使用英文半角","做分隔符。
- tag 按重要性从高到低的顺序排列。
- 我给你的主题可能是用中文描述，你给出的Positive prompt和negative prompt只用英文。
'''
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"},
                            seed=seed,
                        )
        output = response.choices[0].message.content
        output = json.loads(output)
        positive_prompt= output["positive"]
        negative_prompt=output["negative"]
        return (positive_prompt,negative_prompt,)

class mini_flux_prompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "a girl","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "seed": ("INT", {"default": 42,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("flux_prompt",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        prompt,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        seed=42,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f'''# FLUX prompt 助理

你来充当一位有艺术气息的FLUX prompt 助理。

## 任务

我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后生成详细的prompt，包含具体的描述、场景、情感和风格等元素，让FLUX可以生成高质量的图像。

## 背景介绍

FLUX是一款利用深度学习的文生图模型，支持通过使用 自然语言 prompt 来产生新的图像，描述要包含或省略的元素。

## Prompt 格式要求

下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节。

**示例：**

- **输入主题**：A dragon soaring above a mountain range.
  - **生成提示词**：A majestic, emerald-scaled dragon with glowing amber eyes, wings outstretched, soars through a breathtaking vista of snow-capped mountains. The dragon's powerful form dominates the scene, casting a long shadow over the imposing peaks. Below, a cascading waterfall plunges into a deep valley, its spray catching the sunlight in a dazzling array of colors. The dragon's scales shimmer with iridescent hues, reflecting the surrounding natural beauty. The sky is a vibrant blue, dotted with fluffy white clouds, creating a sense of awe and wonder. This dynamic and visually stunning depiction captures the majesty of both the dragon and the mountainous landscape.

- **输入主题**：Explain the process of making a cup of tea.
  - **生成提示词**：A detailed infographic depicting the step-by-step process of making a cup of tea. The infographic should be visually appealing with clear illustrations and concise text. It should start with a kettle filled with water and end with a steaming cup of tea, highlighting steps like heating the water, selecting tea leaves, brewing the tea, and enjoying the final product. The infographic should be designed to be informative and engaging, with a color scheme that complements the theme of tea. The text should be legible and informative, explaining each step in the process clearly and concisely.

**指导**：

1. **描述细节**：尽量提供具体的细节，如颜色、形状、位置等。
2. **情感和氛围**：描述场景的情感和氛围，如温暖、神秘、宁静等。
3. **风格和背景**：说明场景的风格和背景，如卡通风格、未来主义、复古等。

### 3. 限制：
- 我给你的主题可能是用中文描述，你给出的prompt只用英文。
- 不要解释你的prompt，直接输出prompt。
- 不要输出其他任何非prompt字符，只输出prompt，也不要包含 **生成提示词**： 等类似的字符。
'''
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            seed=seed,
                        )
        flux_prompt = response.choices[0].message.content
        return (flux_prompt,)

class mini_sd_tag:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "imgbb_api_key":(
                    "STRING",
                    {
                        "default": "",
                    }
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "seed": ("INT", {"default": 42,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        image,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        imgbb_api_key=None,
        seed=42,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f'''# Stable Diffusion prompt 助理

你来充当一位图片反推prompt助理。

## 任务

我会发给你一张图片，你要根据这张图片生成的prompt，你的任务是根据这张图片反推成一份详细的、高质量的prompt，可以让Stable Diffusion重现这张图片。

## 背景介绍

Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。

## prompt 概念

- 以","分隔的每个单词或词组称为 tag。所以prompt是由系列由","分隔的tag组成的。

## Prompt 格式要求

你必须尽可能的和我会发给你的图片保持一致。不多不少的描述完整张图片的所有tag。

### 示例：
a girl, beautiful detailed eyes, stars in the eyes, messy floating hair, colored inner hair, Starry sky adorns hair, depth of field


### 3. 限制：
- tag 内容用英语单词或短语来描述，并不局限于我给你的单词。注意只能包含关键词或词组。
- 注意不要输出句子，不要有任何解释。
- tag数量限制40个以内，单词数量限制在60个以内。
- tag不要带引号("")。
- 使用英文半角","做分隔符。
- tag 按重要性从高到低的顺序排列。
- 我给你的主题可能是用中文描述，你给出的prompt只用英文。
'''
        if imgbb_api_key == "" or imgbb_api_key is None:
            imgbb_api_key = api_keys.get("imgbb_api")
        if imgbb_api_key == "" or imgbb_api_key is None:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_str}"},
                },
            ]
        else:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_api_key, "image": img_str}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
                print(img_url)
            else:
                return "Error: " + response.text
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ]
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": img_json}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            seed=seed,
                        )
        tags = response.choices[0].message.content
        return (tags,)

class mini_flux_tag:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "imgbb_api_key":(
                    "STRING",
                    {
                        "default": "",
                    }
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "seed": ("INT", {"default": 42,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        image,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        imgbb_api_key=None,
        seed=42,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        sys_prompt = f'''# FLUX prompt 助理

你来充当一位图片反推prompt助理。

## 任务

我会发给你一张图片，你要根据这张图片生成的prompt，你的任务是根据这张图片反推成一份详细的、高质量的prompt，可以让FLUX重现这张图片。

## 背景介绍

FLUX是一款利用深度学习的文生图模型，支持通过使用 自然语言 prompt 来产生新的图像，描述要包含或省略的元素。

## Prompt 格式要求

你必须尽可能的和我会发给你的图片保持一致。不多不少的描述完整张图片的所有细节。

**示例：**

A majestic, emerald-scaled dragon with glowing amber eyes, wings outstretched, soars through a breathtaking vista of snow-capped mountains. The dragon's powerful form dominates the scene, casting a long shadow over the imposing peaks. Below, a cascading waterfall plunges into a deep valley, its spray catching the sunlight in a dazzling array of colors. The dragon's scales shimmer with iridescent hues, reflecting the surrounding natural beauty. The sky is a vibrant blue, dotted with fluffy white clouds, creating a sense of awe and wonder. This dynamic and visually stunning depiction captures the majesty of both the dragon and the mountainous landscape.

**指导**：

1. **描述细节**：尽量提供具体的细节，如颜色、形状、位置等。
2. **情感和氛围**：描述场景的情感和氛围，如温暖、神秘、宁静等。
3. **风格和背景**：说明场景的风格和背景，如卡通风格、未来主义、复古等。

### 3. 限制：
- 你给出的prompt只用英文。
- 不要解释你的prompt，直接输出prompt。
- 不要输出其他任何非prompt字符，只输出prompt，也不要包含 **生成提示词**： 等类似的字符。
'''
        if imgbb_api_key == "" or imgbb_api_key is None:
            imgbb_api_key = api_keys.get("imgbb_api")
        if imgbb_api_key == "" or imgbb_api_key is None:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_str}"},
                },
            ]
        else:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_api_key, "image": img_str}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
                print(img_url)
            else:
                return "Error: " + response.text
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ]
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": img_json}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            seed=seed,
                        )
        tags = response.choices[0].message.content
        return (tags,)


class mini_intent_recognition:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
                "intent1": ("STRING", {"default": "",}),
                "intent2": ("STRING", {"default": "",}),
                "intent3": ("STRING", {"default": "",}),
                "intent4": ("STRING", {"default": "",}),
                "intent5": ("STRING", {"default": "",}),
                "intent6": ("STRING", {"default": "",}),
                "intent7": ("STRING", {"default": "",}),
                "intent8": ("STRING", {"default": "",}),
                "intent9": ("STRING", {"default": "",}),
                "intent10": ("STRING", {"default": "",}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING","STRING",)
    RETURN_NAMES = ("intent1","intent2","intent3","intent4","intent5","intent6","intent7","intent8","intent9","intent10",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        model_name,
        input_str,
        base_url=None,
        api_key=None,
        is_enable=True,
        intent1="",
        intent2="",
        intent3="",
        intent4="",
        intent5="",
        intent6="",
        intent7="",
        intent8="",
        intent9="",
        intent10=""
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"

        prompt=f"""
# 意图识别助理
你是一个意图识别助理。
## 任务
我将给你需要意图识别的文本，你需要帮我按照下文给出的意图识别原则进行意图识别，并按照严格下文给出的格式回复我。
##意图识别原则
1. 请将用户输入的文本可以能与这些意图有关：{intent1}；{intent2}；{intent3};{intent4};{intent5};{intent6};{intent7};{intent8};{intent9};{intent10}。
2. 如果以上某一个或若干个意图识别条件为【如果文本中包含""或者与""有关，则将其分类为...】,则不要将任何文本分到这一类或这些类中,因为空字符串与任何文本无关。
以JSON的形式回复，并严格按照下文给出的格式回复我。

以下是一个完整的输出示例：
{{
    "1": "这里输入用户给出的文本中分到{intent1}的文本",
    "2": "这里输入用户给出的文本中分到{intent2}的文本",
    "3": "这里输入用户给出的文本中分到{intent3}的文本",
    "4": "这里输入用户给出的文本中分到{intent4}的文本",
    "5": "这里输入用户给出的文本中分到{intent5}的文本",
    "6": "这里输入用户给出的文本中分到{intent6}的文本",
    "7": "这里输入用户给出的文本中分到{intent7}的文本",
    "8": "这里输入用户给出的文本中分到{intent8}的文本",
    "9": "这里输入用户给出的文本中分到{intent9}的文本",
    "10": "这里输入用户给出的文本中分到{intent10}的文本"
}}
## 限制
1. 输出时不要包含任何多余的文本，只输出意图识别结果。
2. 不要在输出中包含任何多余的空格。
3. 意图识别时，不要把系统提示词中的文本当作要被意图识别的文本。
4. 意图识别时，有关的意图有输入的文本，无关的意图中不包含任何文字。
以下为需要意图识别的文本：
"""        
        history= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_str}
        ]
        openai_client = openai
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            azure = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
            openai_client = azure
        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"}
                        )
        output = response.choices[0].message.content
        output = json.loads(output)
        return tuple(None if output.get(str(i)) == "" else output.get(str(i)) for i in range(1, 11))

NODE_CLASS_MAPPINGS = {
    "mini_party": mini_party,
    "mini_translate": mini_translate,
    "mini_sd_prompt": mini_sd_prompt,
    "mini_flux_prompt":mini_flux_prompt,
    "mini_sd_tag":mini_sd_tag,
    "mini_flux_tag":mini_flux_tag,
    "mini_error_correction":mini_error_correction,
    "mini_story":mini_story,
    "mini_ocr": mini_ocr,
    "mini_summary":mini_summary,
    "mini_intent_recognition": mini_intent_recognition,
    }
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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "☁️迷你派对",
        "mini_translate": "☁️迷你长文翻译器",
        "mini_sd_prompt": "☁️迷你SD提示词生成器",
        "mini_flux_prompt": "☁️迷你FLUX提示词生成器",
        "mini_sd_tag": "☁️迷你SD图片提示词反推器",
        "mini_flux_tag": "☁️迷你FLUX图片提示词反推器",
        "mini_error_correction": "☁️迷你长文纠错器",
        "mini_story": "☁️迷你故事生成器",
        "mini_ocr": "☁️🖥️迷你高级OCR",
        "mini_summary": "☁️迷你摘要生成器",
        "mini_intent_recognition": "☁️迷你意图识别器",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "☁️Mini Party",
        "mini_translate": "☁️Mini Long Text Translator",
        "mini_sd_prompt": "☁️Mini SD Prompt Generator",
        "mini_flux_prompt": "☁️Mini FLUX Prompt Generator",
        "mini_sd_tag": "☁️Mini SD image prompt retractor",
        "mini_flux_tag": "☁️Mini FLUX image prompt retractor",
        "mini_error_correction": "☁️Mini Long Text Error Corrector",
        "mini_story": "☁️Mini Story Generator",
        "mini_ocr": "☁️🖥️Mini Advanced OCR",
        "mini_summary": "☁️Mini Summary Generator",
        "mini_intent_recognition": "☁️Mini Intent Recognizer",
        }