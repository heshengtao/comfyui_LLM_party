
import requests
from PIL import Image
from io import BytesIO
import json
import locale
import os
import time
import openai
import sounddevice as sd
import torch
import urllib3
import ssl
from PIL import Image, ImageOps, ImageSequence
import numpy as np
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
from openai import OpenAI,AzureOpenAI
config = configparser.ConfigParser()
config.read(config_path)

def process_images(url):
    try:
        # 检查URL是否有效
        if not url or not url.startswith(('http://', 'https://')):
            return "Invalid URL", None

        # 发送GET请求获取图片数据
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果响应包含一个HTTP错误状态码，则抛出异常
        
        # 检查图片格式
        image_data = response.content
        ext = 'JPG' if image_data.startswith(b'\xff\xd8') else ('PNG' if image_data.startswith(b'\x89PNG\r\n\x1a\n') else None)
        if ext is None:
            return "Unknown image extension", None
        
        # 创建临时目录保存图片
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_temp_dir = os.path.join(current_dir, 'img_temp')
        os.makedirs(img_temp_dir, exist_ok=True)

        # 生成唯一的文件名并保存图片
        timestamp = int(time.time())
        img_path = os.path.join(img_temp_dir, f'image-{timestamp}.{ext}')
        with open(img_path, 'wb') as f:
            f.write(image_data)

        # 加载图片并进行预处理
        img = Image.open(img_path)
        img_out = []
        for frame in ImageSequence.Iterator(img):
            frame = ImageOps.exif_transpose(frame)
            if frame.mode == "I":
                frame = frame.point(lambda i: i * (1 / 256)).convert("L")
            image = frame.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image).unsqueeze(0)
            img_out.append(image)
        
        # 返回字符串消息和处理后的图像张量列表中的第一个元素
        return "已经将图片在前端展示", img_out[0] if img_out else None

    except requests.exceptions.RequestException as e:
        return f"Error fetching the image: {e}", None
    except Exception as e:
        return f"An error occurred: {e}", None

class url2img_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "dall_e"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"

    def dall_e(self,is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "process_images",
                    "description": "用于将URL转换为图片，显示到前端展示给用户看。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "你想要展示的图片的URL地址",
                            }
                        },
                        "required": ["url"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)

def path2img(path):
    img = Image.open(path)
    img_out = []
    for frame in ImageSequence.Iterator(img):
        frame = ImageOps.exif_transpose(frame)
        if frame.mode == "I":
            frame = frame.point(lambda i: i * (1 / 256)).convert("L")
        image = frame.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image).unsqueeze(0)
        img_out.append(image)
    img_out = img_out[0]
    return "已经将图片在前端展示",img_out

class path2img_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "dall_e"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"

    def dall_e(self,is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "path2img",
                    "description": "用于将本地path转换为图片，显示到前端展示给用户看。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "你想要展示的图片的URL地址",
                            }
                        },
                        "required": ["path"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)

class openai_dall_e:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "prompt": ("STRING",{"multiline": True}), 
                "image_size": (["1024x1024", "1792x1024", "1024x1792"], {"default": "1024x1024"} ),              
                "image_quality": (["standard", "hd"], {"default": "hd"} ),
                "style": (["vivid", "natural"], {"default": "natural"} ),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE","STRING",)
    RETURN_NAMES = ("img","img_url",)

    FUNCTION = "get_dall_e"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def get_dall_e(self,image_size,image_quality,style,is_enable=True, prompt="", base_url=None, api_key=None):
        if is_enable == False:
            return (None,)
        if api_key != "":
            openai.api_key = api_key
        elif config.get("API_KEYS", "openai_api_key") != "":
            openai.api_key = config.get("API_KEYS", "openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif config.get("API_KEYS", "base_url") != "":
            openai.base_url = config.get("API_KEYS", "base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")
        openai_dall_e = OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            openai_dall_e = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        response = openai_dall_e.images.generate(
            prompt=prompt,
            model="dall-e-3",
            size=image_size,
            quality=image_quality,
            style=style,
            response_format="url",
            n=1,
        )
        # 获取所有生成图像的URL
        image_url = response.data[0].url
        _,img_out=process_images(image_url)
        return (img_out,image_url, )

global_image_size="1024x1024"
global_image_quality="hd"
global_style="natural"
global_dall_e=""
def dall_e(prompt):
    
    global global_image_size, global_image_quality,global_style,global_dall_e
    response = global_dall_e.images.generate(
        prompt=prompt,
        model="dall-e-3",
        size=global_image_size,
        quality=global_image_quality,
        style=global_style,
        response_format="url",
        n=1,
    )
    # 获取所有生成图像的URL
    image_url = response.data[0].url
    _,img_out=process_images(image_url)
    return f"图片已生成：[img]({image_url})",img_out

class dall_e_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "image_size": (["1024x1024", "1792x1024", "1024x1792"], {"default": "1024x1024"} ),              
                "image_quality": (["standard", "hd"], {"default": "hd"} ),
                "style": (["vivid", "natural"], {"default": "natural"} ),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "get_dall_e"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"



    def get_dall_e(self,image_size,image_quality,style,is_enable=True, base_url=None, api_key=None):
        global global_image_size, global_image_quality,global_style,global_dall_e
        global_image_size=image_size
        global_image_quality=image_quality
        global_style=style
        if is_enable == False:
            return (None,)
        if api_key != "":
            openai.api_key = api_key
        elif config.get("API_KEYS", "openai_api_key") != "":
            openai.api_key = config.get("API_KEYS", "openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif config.get("API_KEYS", "base_url") != "":
            openai.base_url = config.get("API_KEYS", "base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")
        global_dall_e = OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            global_dall_e = AzureOpenAI(
                api_key= openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        output = [
            {
                "type": "function",
                "function": {
                    "name": "dall_e",
                    "description": "输入自然语言，生成图片",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "输入用于生成图片的自然语言",
                            }
                        },
                        "required": ["prompt"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)

_TOOL_HOOKS = ["dall_e","process_images","path2img"]
NODE_CLASS_MAPPINGS = {
    "openai_dall_e": openai_dall_e,
    "dall_e_tool":dall_e_tool,
    "url2img_tool":url2img_tool,
    "path2img_tool":path2img_tool,
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
        "openai_dall_e": "☁️dall_e文生图",
        "dall_e_tool": "☁️dall_e文生图工具",
        "url2img_tool": "url转图片工具",
        "path2img_tool": "路径转图片工具",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "openai_dall_e": "☁️Dall_e text2Image",
        "dall_e_tool": "☁️Dall_e text2Image tool",
        "url2img_tool": "url2img tool",
        "path2img_tool": "path2img tool",
    }