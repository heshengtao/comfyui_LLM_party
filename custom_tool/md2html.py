import locale
import re
import markdown
import webbrowser
import os
import sys
import psutil
import time
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
out_path = os.path.join(current_dir,"output")
# 确保输出目录存在
if not os.path.exists(out_path):
    os.makedirs(out_path)

def is_html_string(s):
    html_pattern = re.compile(r'<([A-Za-z][A-Za-z0-9]*)\b[^>]*>(.*?)<\/\1>')
    return bool(html_pattern.search(s))

import mdtex2html

def markdown_to_html(md_text):
    # Convert Markdown to HTML with math support
    html = mdtex2html.convert(md_text, extensions=['extra'])
    
    # Insert the HTML into the HTML template
    html_template = """
<html>
<head>
    <style>
        body {{
            font-family: "Source Sans Pro", sans-serif;
            font-size: 16px;
            line-height: 1.5;
            margin: 20px;
            background-color: #FFFFFF;
            color: #262730;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #262730; /* 纯黑色 */
            font-weight: bold;
        }}
        ul, ol {{
            padding-left: 20px;
        }}
        pre {{
            background-color: #F0F2F6;
            padding: 10px;
            border-radius: 5px;
            overflow: auto;
            position: relative;
        }}
        code {{
            background-color: #F0F2F6;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .blockformula {{
            text-align: center;
            margin: 1em 0;
        }}
        table {{
            width: 80%;
            margin: 20px auto; /* 居中表格 */
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #F2F2F2;
        }}
        tr:nth-child(even) {{
            background-color: #F9F9F9;
        }}
        tr:hover {{
            background-color: #F1F1F1;
        }}
        .button, .label {{
            position: absolute;
            top: 5px;
            background-color: #E0E0E0;
            color: black;
            border: none;
            padding: 5px;
            cursor: pointer;
            border-radius: 3px;
            font-size: 12px;
        }}
        .button:hover, .label:hover {{
            background-color: #D0D0D0;
        }}
        .button {{
            right: 5px;
        }}
        .label {{
            left: 5px;
            padding: 2px 5px;
        }}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
    <script>
        hljs.highlightAll();
        document.addEventListener('DOMContentLoaded', (event) => {{
            document.querySelectorAll('pre code').forEach((block) => {{
                const button = document.createElement('button');
                button.innerText = 'Copy';
                button.className = 'button';
                button.addEventListener('click', () => {{
                    navigator.clipboard.writeText(block.innerText).then(() => {{
                        button.innerText = 'Copied!';
                        setTimeout(() => {{
                            button.innerText = 'Copy';
                        }}, 2000);
                    }});
                }});
                block.parentNode.appendChild(button);

                const language = block.className.split('-')[1];
                if (language) {{
                    const label = document.createElement('span');
                    label.innerText = language.toUpperCase();
                    label.className = 'label';
                    block.parentNode.appendChild(label);
                }}
            }});
        }});
    </script>
</head>
<body>
    {html_content}
</body>
</html>
"""
    html_content = html_template.format(html_content=html)
    return html_content

class Browser_display:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "md_or_html": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("log",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/文本（text）"
    OUTPUT_NODE = True

    def convert_txt2json(self,md_or_html, is_enable=True):
        if is_enable == False:
            return (None,)
        if is_html_string(md_or_html):
            html_content = md_or_html
        else:
            html_content = markdown_to_html(md_or_html)
        path = os.path.join(out_path, "md_to_html.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        try:
            # 如果没有打开文件，则使用默认浏览器打开
            webbrowser.open(path)
        except Exception as e:
            return (f"打开网页时出错: {str(e)}",)
        return ("成功打开网页",)



class md_to_html:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "md_str": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("HTML",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def time(self, md_str, is_enable=True):
        if is_enable == False:
            return (None,)
        return (markdown_to_html(md_str),)
        


NODE_CLASS_MAPPINGS = {"md_to_html": md_to_html,"Browser_display": Browser_display,}
# 获取系统语言
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'

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
    NODE_DISPLAY_NAME_MAPPINGS = {
        "md_to_html": "Markdown转HTML",
        "Browser_display": "浏览器显示"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "md_to_html": "Markdown to HTML",
        "Browser_display": "Browser display"}