import json
import os
from ..config import current_dir_path
import numpy as np
from PIL import Image, ImageOps, ImageSequence
import torch
import docx2txt
import openpyxl
import pandas as pd
import xlrd

programming_languages_extensions = [
    ".py", ".js", ".java", ".c", ".cpp", ".html", ".css", ".sql", ".r", ".swift"
]

def read_one(path):
    text=""
    if path.endswith(".docx"):
        text += docx2txt.process(path)
    elif path.endswith(".xlsx"):
        workbook = openpyxl.load_workbook(path)
        for sheet in workbook:
            for row in sheet.iter_rows(values_only=True):
                text += ' '.join([str(cell) for cell in row if cell is not None]) + ' '
    elif path.endswith(".xls"):
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        for row_num in range(sheet.nrows):
            text += ' '.join([str(cell) for cell in sheet.row_values(row_num)]) + ' '
    elif path.endswith(".csv"):
        df = pd.read_csv(path, encoding='utf-8')
        text += df.to_string(header=False, index=False)
    elif path.endswith(".txt"):
        with open(path, 'r', encoding='utf-8') as f:
            text += f.read()
    elif any(path.endswith(extension) for extension in programming_languages_extensions):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                text += file.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as file:
                text += file.read()
    
    return text



file_path = os.path.join(current_dir_path, 'file')

class load_file:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {
                    "default": "test.txt"
                }),
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),
                "path_type":(["Absolute_Path","Relative_Path"],{
                    "default":"Relative_Path"
                })
            },
            "optional": {

            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"



    def file(self,path,path_type,is_enable="enable"):
        if is_enable=="disable":
            return (None,)
        if path_type=="Absolute_Path":
            path = path
        else:
            path = os.path.join(file_path, path)
        out=read_one(path)
        return (out,)
    



# 定义一个函数，将图片路径转换为与 save_images 函数兼容的格式
def convert_image_to_compatible_format(image_path):
    # 从给定路径加载图片
    img = Image.open(image_path).convert('RGB')
    
    # 将图片转换为numpy数组并归一化
    img_array = np.asarray(img) / 255.
    
    # 将numpy数组转换为torch张量
    img_tensor = torch.tensor(img_array).permute(2, 0, 1).unsqueeze(0)  # 调整维度顺序并添加批次维度
    
    # 返回预期格式的张量
    return img_tensor



class start_workflow:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {

            },
            "optional": {
                "file_path": ("STRING", {
                    "default": None
                }),
                "img_path": ("STRING", {
                    "default": None,
                    "image_upload": True
                }),
                "system_prompt": ("STRING", {
                    "default": "你是一个强大的智能助手"
                }),
                "user_prompt": ("STRING", {
                    "default": "你好"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING","IMAGE","STRING","STRING",)
    RETURN_NAMES = ("file_content","image","system_prompt","user_prompt",)

    FUNCTION = "load_all"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/API"



    def load_all(self,file_path=None,img_path=None,system_prompt="你是一个强大的智能助手",user_prompt="你好"):
        file_out=""
        if file_path is not None and file_path !="":
            path = os.path.join(file_path, path)
            file_out=read_one(path)
        img_out = []
        if img_path is not None and img_path !="":
            img = Image.open(img_path)
            for i in ImageSequence.Iterator(img):
                i = ImageOps.exif_transpose(i)
                if i.mode == 'I':
                    i = i.point(lambda i: i * (1 / 255))
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
                img_out.append(image)
            if len(img_out) > 1:
                img_out= torch.cat(img_out, dim=0)
            else:
                img_out = img_out[0]
        return (file_out,img_out,system_prompt,user_prompt,)