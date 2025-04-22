

import locale


def generate_mermaid(graph_definition,mode="dark"):

    if mode=="dark":
        mermaid_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    background-color: #000000;
                }}
                .mermaid {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .node rect {{
                    fill: #FFFFFF;
                    stroke: #FFD700;
                    stroke-width: 2px;
                    rx: 20;  /* 增加圆角程度 */
                    ry: 20;  /* 增加圆角程度 */
                }}
                .node text {{
                    fill: #000000;
                    font-family: 'Arial, sans-serif';
                    font-size: 16px;
                }}
                .edgePath path {{
                    stroke: #FFD700;
                }}
            </style>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'base',
                    themeVariables: {{
                        primaryColor: '#FFFFFF',
                        primaryTextColor: '#000000',
                        primaryBorderColor: '#FFD700',
                        lineColor: '#FFD700',
                        backgroundColor: '#000000',
                        fontFamily: 'Arial, sans-serif',
                        fontSize: '16px'
                    }}
                }});
                document.addEventListener('DOMContentLoaded', () => {{
                    const nodes = document.querySelectorAll('.node rect');
                    nodes.forEach(node => {{
                        const text = node.nextElementSibling;
                        const textWidth = text.getBBox().width;
                        const textHeight = text.getBBox().height;
                        const minWidth = 2 * textHeight;
                        const newWidth = Math.max(minWidth, textWidth * 1.2);
                        node.setAttribute('width', newWidth);
                        node.setAttribute('x', -newWidth / 2);
                    }});
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
                {graph_definition}
            </div>
        </body>
        </html>
        """
    elif mode=="light":
        mermaid_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    background-color: #FFFFFF;
                }}
                .mermaid {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .node rect {{
                    fill: #FFD700;
                    stroke: #000000;
                    stroke-width: 2px;
                    rx: 20;  /* 增加圆角程度 */
                    ry: 20;  /* 增加圆角程度 */
                }}
                .node text {{
                    fill: #000000;
                    font-family: 'Arial, sans-serif';
                    font-size: 16px;
                }}
                .edgePath path {{
                    stroke: #000000;
                }}
            </style>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'base',
                    themeVariables: {{
                        primaryColor: '#FFD700',
                        primaryTextColor: '#000000',
                        primaryBorderColor: '#000000',
                        lineColor: '#000000',
                        backgroundColor: '#FFFFFF',
                        fontFamily: 'Arial, sans-serif',
                        fontSize: '16px'
                    }}
                }});
                document.addEventListener('DOMContentLoaded', () => {{
                    const nodes = document.querySelectorAll('.node rect');
                    nodes.forEach(node => {{
                        const text = node.nextElementSibling;
                        const textWidth = text.getBBox().width;
                        const textHeight = text.getBBox().height;
                        const minWidth = 2 * textHeight;
                        const newWidth = Math.max(minWidth, textWidth * 1.2);
                        node.setAttribute('width', newWidth);
                        node.setAttribute('x', -newWidth / 2);
                    }});
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
                {graph_definition}
            </div>
        </body>
        </html>
        """
    elif mode=="dtransparent":
        mermaid_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    background-color: transparent;
                }}
                .mermaid {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .node rect {{
                    fill: #FFD700;
                    stroke: #000000;
                    stroke-width: 2px;
                    rx: 20;  /* 增加圆角程度 */
                    ry: 20;  /* 增加圆角程度 */
                }}
                .node text {{
                    fill: #000000;
                    font-family: 'Arial, sans-serif';
                    font-size: 16px;
                }}
                .edgePath path {{
                    stroke: #000000;
                }}
            </style>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'base',
                    themeVariables: {{
                        primaryColor: '#FFD700',
                        primaryTextColor: '#000000',
                        primaryBorderColor: '#000000',
                        lineColor: '#000000',
                        backgroundColor: 'transparent',
                        fontFamily: 'Arial, sans-serif',
                        fontSize: '16px'
                    }}
                }});
                document.addEventListener('DOMContentLoaded', () => {{
                    const nodes = document.querySelectorAll('.node rect');
                    nodes.forEach(node => {{
                        const text = node.nextElementSibling;
                        const textWidth = text.getBBox().width;
                        const textHeight = text.getBBox().height;
                        const minWidth = 2 * textHeight;
                        const newWidth = Math.max(minWidth, textWidth * 1.2);
                        node.setAttribute('width', newWidth);
                        node.setAttribute('x', -newWidth / 2);
                    }});
                }});
            </script>
        </head>
        <body>
            <div class="mermaid">
                {graph_definition}
            </div>
        </body>
        </html>
        """
    return mermaid_html

class graph_md_to_html:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "graph_definition": ("STRING", {"forceInput": True}),
                "mode": (["dark","light","dtransparent"], {"default": "dark"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("HTML",)

    FUNCTION = "time"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def time(self, graph_definition,mode, is_enable=True):
        if is_enable == False:
            return (None,)
        html=generate_mermaid(graph_definition,mode)
        return (html,)

NODE_CLASS_MAPPINGS = {"graph_md_to_html": graph_md_to_html}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"graph_md_to_html": "思维导图markdown转HTML"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"graph_md_to_html": "graph markdown to HTML"}
