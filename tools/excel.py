import hashlib
import json
import os
import time

import pandas as pd


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
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, path, is_enable=True, is_reload=False):
        if not is_enable:
            return (None,)
        if self.path != path or is_reload == True:
            self.index = 0  # 重置索引为0，因为我们要从第二行开始读取数据
            self.path = path
        # 使用pandas读取Excel文件，header=0表示第一行作为列名
        df = pd.read_excel(self.path, header=0)
        # 检查是否有足够的行可以读取
        if self.index < len(df):
            # 读取第self.index行的数据
            data_row = df.iloc[self.index]
            # 将Series对象转换为字典
            data_dict = data_row.to_dict()
            # 返回JSON格式的数据
            data = json.dumps(data_dict, ensure_ascii=False)
            # 增加索引，准备读取下一行
            self.index += 1
            return (data,)
        else:
            # 如果没有更多的行可以读取，返回None
            return (None,)

    @classmethod
    def IS_CHANGED(self, s):
        self.record = self.index
        return self.record
