import locale
import os
from html2image import Html2Image
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import torch

# 获取当前目录路径
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 在current_dir_path下创建一个名为output的文件夹
output_dir_path = os.path.join(current_dir_path, 'output')
os.makedirs(output_dir_path, exist_ok=True)

def save_svg_code_to_html(svg_code, html_file):
    html_str = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Example</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            svg {{
                width: 100%;
                height: 100%;
                max-width: 100%;
                max-height: 100%;
            }}
        </style>
    </head>
    <body>
        <?xml version="1.0" encoding="UTF-8"?>
        {svg_code}
    </body>
    </html>
    '''
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_str)

def html2img(html_file, output_file, width=800, height=600):
    hti = Html2Image()
    hti.output_path = output_dir_path
    hti.screenshot(html_file=html_file, save_as=output_file, size=(width, height))
    image_path = os.path.join(hti.output_path, output_file)
    return image_path

class svg2html:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "svg_code": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("html_str",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def time(self, svg_code, is_enable=True):
        if is_enable == False:
            return (None,)
        html_str = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Example</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        svg {{
            width: 100%;
            height: 100%;
            max-width: 100%;
            max-height: 100%;
        }}
    </style>
</head>
<body>
    <?xml version="1.0" encoding="UTF-8"?>
    {svg_code}
</body>
</html>
'''
        return (html_str,)

class svg2img_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "svg_str": ("STRING", {"forceInput": True}),
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

    def time(self, svg_str, width, height, is_enable=True):
        if is_enable == False:
            return (None,)
        img_out = []

        # 保存SVG代码为HTML文件
        html_file = os.path.join(output_dir_path, 'example.html')
        save_svg_code_to_html(svg_str, html_file)

        # 将HTML文件转换为PNG图像
        png_file = 'example.png'
        image_path = html2img(html_file, png_file, width, height)
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


NODE_CLASS_MAPPINGS = {"svg2img_function": svg2img_function,
                      "svg2html": svg2html}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"svg2img_function": "SVG转图片",
                                  "svg2html": "SVG转HTML"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"svg2img_function": "SVG to Image",
                                  "svg2html": "SVG to HTML"}