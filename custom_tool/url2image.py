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
                "url": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING","IMAGE", "STRING",)
    RETURN_NAMES = ("file_path","img", "log",)

    FUNCTION = "url_to_img"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def url_to_img(self, url, is_enable=True):
        if not is_enable:
            return (None, None, "Function is disabled")
            
        if not url:
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

        img_path = f'image.{ext}'
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
        return (img_path, img_out, f"Image file saved as {img_path}")

NODE_CLASS_MAPPINGS = {
    "URL2IMG": URL2IMG,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "URL2IMG": "下载图片🐶（URL2IMG）",
}
