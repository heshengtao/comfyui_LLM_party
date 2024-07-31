import os
import requests
import torch
import urllib3
import ssl
from PIL import Image, ImageOps, ImageSequence
import numpy as np
class URL2IMG:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {})
            }
        }

    RETURN_TYPES = ("STRING","IMAGE", "STRING",)
    RETURN_NAMES = ("file_path","img", "log",)

    FUNCTION = "url_to_img"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def url_to_img(self, url):
        if url is None or url=="":
            return (None, None,"url is None",)
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')

        http = urllib3.PoolManager(ssl_context=context)

        response = http.request('GET', url)

        if response.status >= 300:
            print("Failed to get data from url")
            return (None, "Failed to get data from url",)

        first_bytes = response.data[:8]

        if first_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            ext = 'PNG'
        elif first_bytes.startswith(b'\xff\xd8'):
            ext = 'JPG'
        else:
            return (None, "unknown img ext according base64")

        img_path = f'image.{ext}'
        with open(img_path, 'wb') as f:
            f.write(response.data)

        img_out = []
        if img_path is not None:
            for image in img_path:
                img_out.append(image)
        if img_path is not None and img_path != "":
            # 检查img_path是否是一个目录
            if os.path.isdir(img_path):
                # 遍历目录中的所有文件
                for filename in os.listdir(img_path):
                    # 检查文件是否是图片
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
                        img_full_path = os.path.join(img_path, filename)
                        img = Image.open(img_full_path)
                        img = ImageOps.exif_transpose(img)
                        if img.mode == "I":
                            img = img.point(lambda i: i * (1 / 256)).convert("L")
                        image = img.convert("RGB")
                        image = np.array(image).astype(np.float32) / 255.0
                        image = torch.from_numpy(image).unsqueeze(0)
                        img_out.append(image)
            else:
                img = Image.open(img_path)
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
        return (img_path,img_out, f"Image file saved as {img_path}")

NODE_CLASS_MAPPINGS = {
    "URL2IMG": URL2IMG,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "URL2IMG": "下载图片🐶（URL2IMG）",
}
