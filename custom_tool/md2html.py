import locale
import markdown

def markdown_to_html(md_text):
    # Convert Markdown to HTML
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
    # 把HTML插入到HTML模板中
    html_template = """
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            margin: 20px;
            background-color: white; /* 设置背景颜色 */
            color: black; /* 设置字体颜色 */
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-weight: bold;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow: auto;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body>
    {html_content}
</body>
</html>
"""
    html_content = html_template.format(html_content=html)
    return html_content

class md_to_html:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "md_str": ("STRING", {"default": "md code string"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("HTML",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def time(self, md_str, is_enable=True):
        if is_enable == False:
            return (None,)
        return (markdown_to_html(md_str),)
        


NODE_CLASS_MAPPINGS = {"md_to_html": md_to_html}
# 获取系统语言
lang = locale.getdefaultlocale()[0]
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
    NODE_DISPLAY_NAME_MAPPINGS = {"md_to_html": "Markdown转HTML"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"md_to_html": "Markdown to HTML"}