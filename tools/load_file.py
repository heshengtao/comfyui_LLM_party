import json
import os
from ..config import current_dir_path

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