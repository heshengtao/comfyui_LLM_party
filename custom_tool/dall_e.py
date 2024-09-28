
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
from openai import OpenAI
config = configparser.ConfigParser()
config.read(config_path)

def process_images(url):
    if url is None or "http" not in url:
        return (None, None, "URL is None")

    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT@SECLEVEL=1')
    http = urllib3.PoolManager(ssl_context=context)

    response = http.request('GET', url)
    if response.status >= 300:
        return (None, None, "Failed to get data from URL")

    first_bytes = response.data[:8]
    if first_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        ext = 'PNG'
    elif first_bytes.startswith(b'\xff\xd8'):
        ext = 'JPG'
    else:
        return (None, None, "Unknown image extension based on base64")
    # 当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建img_temp目录路径
    img_temp_dir = os.path.join(current_dir, 'img_temp')
    # 如果img_temp目录不存在，则创建
    os.makedirs(img_temp_dir, exist_ok=True)
    # 时间戳
    timestamp = int(time.time())
    img_path = os.path.join(img_temp_dir,f'image-{timestamp}.{ext}')
    with open(img_path, 'wb') as f:
        f.write(response.data)

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
    img_out = img_out[0]
    return img_out


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

    FUNCTION = "dall_e"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/音频（audio）"




    def dall_e(self,image_size,image_quality,style,is_enable=True, prompt="", base_url=None, api_key=None):
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
        if openai.api_key == "":
            return ("请输入API_KEY",)
        openai_dall_e = OpenAI(api_key=openai.api_key, base_url=openai.base_url)
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
        img_out=process_images(image_url)
        return (img_out,image_url, )

NODE_CLASS_MAPPINGS = {
    "openai_dall_e": openai_dall_e,
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
        "openai_dall_e": "dall_e文生图",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "openai_dall_e": "Dall_e text2Image",
    }