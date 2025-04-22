import locale
import os
import pandas as pd
from io import StringIO
import markdown


def md2excel(markdown_data, output_file):
    # 将Markdown转换为HTML
    html_data = markdown.markdown(markdown_data, extensions=['tables'])

    print(html_data)

    # 使用StringIO包装HTML字符串
    html_io = StringIO(html_data)

    # 使用Pandas解析HTML表格
    markdown_table = pd.read_html(html_io)[0]

    # 将解析结果保存为Excel文件
    markdown_table.to_excel(output_file, index=False)

class md_to_excel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "md_str": ("STRING", {"forceInput": True}),
                "output_file": ("STRING", {"default": "output.xlsx"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log",)

    FUNCTION = "time"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def time(self, md_str,output_file, is_enable=True):
        if is_enable == False:
            return (None,)
        md2excel(md_str,output_file)
        return ("Markdown表格已成功转换为Excel文件！",)
        


NODE_CLASS_MAPPINGS = {"md_to_excel": md_to_excel}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"md_to_excel": "markdown转excel"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"md_to_excel": "markdown to excel"}