import hashlib
import json
import os
import random
import time
import datetime

import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageFile, ImageOps, ImageSequence, UnidentifiedImageError
import signal
import sys

def interrupt_handler(signum, frame):
    print("Process interrupted")
    sys.exit(0)

def pillow(fn, arg):
    prev_value = None
    try:
        x = fn(arg)
    except (OSError, UnidentifiedImageError, ValueError):  # PIL issues #4472 and #2445, also fixes ComfyUI issue #3416
        prev_value = ImageFile.LOAD_TRUNCATED_IMAGES
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        x = fn(arg)
    finally:
        if prev_value is not None:
            ImageFile.LOAD_TRUNCATED_IMAGES = prev_value
        return x

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)

class load_excel:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.path = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "test.xlsx"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "load_all": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential","random","Infinite", "sequential_flagout"], {"default": "sequential"}),
            },
            "optional": {
                "start_row": ("INT", {"default": 2, "min": 2, "max": 1048576}),
                "end_row": ("INT", {"default": 1048576, "min": 2, "max": 1048576}),
            },
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("file_content", "is_end")

    FUNCTION = "file"

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, path, iterator_mode, is_enable=True, is_reload=False, load_all=False,start_row=2, end_row=1048576):
        flag_is_end = False
        if not is_enable:
            return (None, flag_is_end,)   
        if load_all:
            # 返回这个表格，以json字符串格式返回
            df = pd.read_excel(path, header=0)
            data_list = df.to_dict(orient='records')
            data = json.dumps(data_list, ensure_ascii=False, indent=4, cls=DateTimeEncoder)
            return (data, flag_is_end,)
        if self.index < start_row - 2:
            self.index = start_row - 2  # 重置索引为0，因为我们要从第二行开始读取数据
        if self.path != path or is_reload == True:
            self.index = start_row - 2  # 重置索引为0，因为我们要从第二行开始读取数据
            self.path = path
        # 使用pandas读取Excel文件，header=0表示第一行作为列名
        df = pd.read_excel(self.path, header=0)
        # 检查是否有足够的行可以读取
        if self.index >= len(df) or self.index >= end_row - 1:
            self.index = start_row - 2  # 重置索引为0，因为我们要从第二行开始读取数据
            if iterator_mode == "sequential":
                signal.signal(signal.SIGINT, interrupt_handler)
                signal.raise_signal(signal.SIGINT)  # 直接中断进程
        if (self.index == len(df) - 1 or self.index == end_row - 2) and iterator_mode == "sequential_flagout":
            flag_is_end = True
        # 读取第self.index行的数据
        data_row = df.iloc[self.index]
        # 将Series对象转换为字典
        data_dict = data_row.to_dict()
        # 返回JSON格式的数据
        data = json.dumps(data_dict, ensure_ascii=False, indent=4, cls=DateTimeEncoder)
        if iterator_mode == "sequential" or iterator_mode == "Infinite" or iterator_mode == "sequential_flagout":
            self.index += 1
        elif iterator_mode == "random":
            self.index = random.randint(start_row - 2,end_row - 2)
        return (data, flag_is_end,)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record

# 其他类的定义保持不变
class image_iterator:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.path = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential","random","Infinite", "sequential_flagout"], {"default": "sequential"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN")
    RETURN_NAMES = ("image", "is_end")

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, folder_path,iterator_mode, is_enable=True, is_reload=False):
        flag_is_end = False
        if not is_enable:
            return (None, flag_is_end,)
        if self.path != folder_path or is_reload == True:
            self.index = 0  # 重置索引为0，因为我们要从第二行开始读取数据
            self.path = folder_path
        # 将文件夹里的所有图片按修改时间排序，
        image_files = sorted(
            [f for f in os.listdir(folder_path) if f.lower().endswith((
                ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg", ".ico", ".raw"
            ))]
        )
        # 读取第self.index个图片
        # 如果没有更多的图片可以读取，返回None

        if self.index >= len(image_files):
            self.index = 0
            if iterator_mode == "sequential":
                signal.signal(signal.SIGINT, interrupt_handler)
                signal.raise_signal(signal.SIGINT)  # 直接中断进程
        if self.index == len(image_files) - 1 and iterator_mode == "sequential_flagout":
            flag_is_end = True
        image_path = os.path.join(folder_path, image_files[self.index])
        img = pillow(Image.open, image_path)

        output_images = []
        w, h = None, None

        excluded_formats = ["MPO"]

        for i in ImageSequence.Iterator(img):
            i = pillow(ImageOps.exif_transpose, i)

            if i.mode == "I":
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]

            if image.size[0] != w or image.size[1] != h:
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
        else:
            output_image = output_images[0]
        if iterator_mode == "sequential" or iterator_mode =="Infinite" or iterator_mode == "sequential_flagout":
            self.index += 1
        elif iterator_mode == "random":
            self.index = random.randint(0, len(image_files) - 1)
        return (output_image, flag_is_end,)
    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record

# 其他类的定义保持不变
class file_path_iterator:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.path = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
                "extension": ("STRING", {"default": ".png,.jpg,.jpeg,.gif,.bmp"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential","random","Infinite", "sequential_flagout"], {"default": "sequential"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("file_path", "is_end")

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, folder_path,iterator_mode,extension, is_enable=True, is_reload=False):
        flag_is_end = False
        if not is_enable:
            return (None, flag_is_end,)
        if self.path != folder_path or is_reload == True:
            self.index = 0  # 重置索引为0，因为我们要从第二行开始读取数据
            self.path = folder_path
        extension = extension.split(",")
        # 将文件夹里的所有图片按修改时间排序，
        image_files = sorted(
            [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extension))],
        )
        # 读取第self.index个图片
        # 如果没有更多的图片可以读取，返回None

        if self.index >= len(image_files):
            self.index = 0
            if iterator_mode == "sequential":
                signal.signal(signal.SIGINT, interrupt_handler)
                signal.raise_signal(signal.SIGINT)  # 直接中断进程
        if self.index == len(image_files) - 1 and iterator_mode == "sequential_flagout":
            flag_is_end = True
        image_path = os.path.join(folder_path, image_files[self.index])

        if iterator_mode == "sequential" or iterator_mode =="Infinite" or iterator_mode == "sequential_flagout":
            self.index += 1
        elif iterator_mode == "random":
            self.index = random.randint(0, len(image_files) - 1)
        return (image_path, flag_is_end,)
    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record


class json_iterator:
    def __init__(self):
        self.index = 0
        self.record = 0
        self.json_str = None
        self.data = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_str": ("STRING", {"default": '{"key": "value"}'}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "is_reload": ("BOOLEAN", {"default": False}),
                "load_all": ("BOOLEAN", {"default": False}),
                "iterator_mode": (["sequential","random","Infinite", "sequential_flagout"], {"default": "sequential"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("file_content", "is_end")

    FUNCTION = "file"

    CATEGORY = "大模型派对（llm_party）/迭代器（iterator）"

    def file(self, json_str,iterator_mode, is_enable=True, is_reload=False, load_all=False):
        flag_is_end = False
        if not is_enable:
            return (None, flag_is_end)
        if self.json_str != json_str or is_reload:
            self.index = 0  # 重置索引为0
            self.json_str = json_str
            self.data = json.loads(self.json_str)
        
        if load_all:
            # 返回整个JSON数据作为字符串
            return (json.dumps(self.data, ensure_ascii=False, indent=4), flag_is_end)
        
        if isinstance(self.data, list):
            if self.index >= len(self.data):
                self.index=0
                if iterator_mode == "sequential":
                    signal.signal(signal.SIGINT, interrupt_handler)
                    signal.raise_signal(signal.SIGINT)  # 直接中断进程
            if self.index == len(self.data) - 1 and iterator_mode == "sequential_flagout":
                flag_is_end = True
            data_item = self.data[self.index]
            if iterator_mode == "sequential" or iterator_mode =="Infinite" or iterator_mode =="sequential_flagout":
                self.index += 1
            elif iterator_mode == "random":
                self.index = random.randint(0, len(self.data) - 1)
            return (json.dumps(data_item, ensure_ascii=False, indent=4), flag_is_end)

        
        elif isinstance(self.data, dict):
            keys = list(self.data.keys())
            if self.index >= len(keys):
                self.index=0
                if iterator_mode == "sequential":
                    signal.signal(signal.SIGINT, interrupt_handler)
                    signal.raise_signal(signal.SIGINT)  # 直接中断进程
            if self.index == len(self.data) - 1 and iterator_mode == "sequential_flagout":
                flag_is_end = True
            key = keys[self.index]
            data_item = self.data[key]
            if iterator_mode == "sequential" or iterator_mode =="Infinite"  or iterator_mode =="sequential_flagout":
                self.index += 1
            elif iterator_mode == "random":
                self.index = random.randint(0, len(self.data) - 1)
            return (json.dumps(data_item, ensure_ascii=False, indent=4), flag_is_end)
        
        return (None, flag_is_end)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record