import json
import os

import docx2txt
import numpy as np
import openpyxl
import pandas as pd
import pdfplumber
import requests
import torch
import xlrd
from PIL import Image, ImageOps, ImageSequence

from ..config import current_dir_path

programming_languages_extensions = [".py", ".js", ".java", ".c", ".cpp", ".html", ".css", ".sql", ".r", ".swift"]


def read_one(path):
    text = ""
    if path.endswith(".docx"):
        text += docx2txt.process(path)
    elif path.endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif path.endswith(".xlsx"):
        workbook = openpyxl.load_workbook(path)
        for sheet in workbook:
            for row in sheet.iter_rows(values_only=True):
                text += " ".join([str(cell) for cell in row if cell is not None]) + " "
    elif path.endswith(".xls"):
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        for row_num in range(sheet.nrows):
            text += " ".join([str(cell) for cell in sheet.row_values(row_num)]) + " "
    elif path.endswith(".csv"):
        df = pd.read_csv(path, encoding="utf-8")
        text += df.to_string(header=False, index=False)
    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text += f.read()
    elif any(path.endswith(extension) for extension in programming_languages_extensions):
        try:
            with open(path, "r", encoding="utf-8") as file:
                text += file.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="latin-1") as file:
                text += file.read()

    return text


file_path = os.path.join(current_dir_path, "file")


class load_file:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": "test.txt"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "path_type": (["Absolute_Path", "Relative_Path"], {"default": "Relative_Path"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, path, path_type, is_enable=True):
        if is_enable == False:
            return (None,)
        if path_type == "Absolute_Path":
            path = path
        else:
            path = os.path.join(file_path, path)
        out = read_one(path)
        return (out,)


class load_file_folder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "C://Users/"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, folder_path, is_enable=True):
        if is_enable == False:
            return (None,)
        # 获取文件夹中的所有文件，并读取到字符串中
        out = ""
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                out += read_one(file_path)
        return (out,)


class load_url:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"default": "https://example.com"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, url, is_enable=True):
        if is_enable == False:
            return (None,)
        try:

            jina = "https://r.jina.ai/"
            url = jina + url

            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 确保请求成功

            # 设置响应内容的编码，确保文本不会出现编码问题
            response.encoding = response.apparent_encoding
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return (None,)
        out = response.text
        return (out,)


# 定义一个函数，将图片路径转换为与 save_images 函数兼容的格式
def convert_image_to_compatible_format(image_path):
    # 从给定路径加载图片
    img = Image.open(image_path).convert("RGB")

    # 将图片转换为numpy数组并归一化
    img_array = np.asarray(img) / 255.0

    # 将numpy数组转换为torch张量
    img_tensor = torch.tensor(img_array).permute(2, 0, 1).unsqueeze(0)  # 调整维度顺序并添加批次维度

    # 返回预期格式的张量
    return img_tensor


class start_workflow:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "image_input": ("IMAGE", {}),
                "file_path": ("STRING", {"default": None}),
                "img_path": ("STRING", {"default": None, "image_upload": True}),
                "system_prompt": ("STRING", {"default": "你是一个强大的智能助手"}),
                "user_prompt": ("STRING", {"default": "你好"}),
                "positive_prompt": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "IMAGE",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "file_content",
        "image",
        "system_prompt",
        "user_prompt",
        "positive_prompt",
        "negative_prompt",
    )

    FUNCTION = "load_all"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def load_all(
        self,
        file_content="",
        image_input=None,
        file_path=None,
        img_path=None,
        system_prompt="你是一个强大的智能助手",
        user_prompt="你好",
        positive_prompt="",
        negative_prompt="",
    ):
        file_out = ""
        if file_content is not None and file_content != "":
            file_out += file_content
        if file_path is not None and file_path != "":
            if os.path.isdir(file_path):
                for path in os.listdir(file_path):
                    path = os.path.join(file_path, path)
                    file_out += read_one(path) + "/n/n"
            else:
                path = os.path.join(file_path, path)
                file_out = read_one(path)
        img_out = []
        if image_input is not None:
            for image in image_input:
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

        system_out = system_prompt
        user_out = user_prompt
        positive_out = positive_prompt
        negative_out = negative_prompt
        return (
            file_out,
            img_out,
            system_out,
            user_out,
            positive_out,
            negative_out,
        )
