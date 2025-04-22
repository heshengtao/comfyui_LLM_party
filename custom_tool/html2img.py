import locale
import os
from html2image import Html2Image
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 在current_dir_path下创建一个名为output的文件夹
output_dir_path = os.path.join(current_dir_path, 'output')

def html2img(html_str, width=800, height=600):
    hti = Html2Image(custom_flags=['--no-sandbox'])
    hti.output_path = output_dir_path
    hti.screenshot(html_str=html_str, save_as='example.png', size=(width, height))
    image_path = os.path.join(hti.output_path, 'example.png')
    return image_path

class html2img_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "html_str": ("STRING", {"forceInput": True}),
                "width": ("INT", {"default": 800}),
                "height": ("INT", {"default": 600}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("img",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def time(self, html_str, width, height, is_enable=True):
        if is_enable == False:
            return (None,)
        img_out = []
        image_path = html2img(html_str, width, height)
        img = Image.open(image_path)
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 256)).convert("L")
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image).unsqueeze(0)
            img_out.append(image)

        if len(img_out) > 1:
            img_out = torch.cat(img_out, dim=0)
        elif img_out:
            img_out = img_out[0]
        if img_out == []:
            img_out = None
        return (img_out,)


NODE_CLASS_MAPPINGS = {"html2img_function": html2img_function}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"html2img_function": "HTML转图片"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"html2img_function": "HTML to Image"}