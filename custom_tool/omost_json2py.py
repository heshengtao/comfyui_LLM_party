# 将 JSON 数据转换为字典
import json
import locale
def json_to_py(json_data):
    data = json.loads(json_data)

    # 初始化 Python 代码字符串
    python_code = """
# Initialize the canvas
canvas = Canvas()

# Set a global description for the canvas
canvas.set_global_description(
    description="{description}",
    detailed_descriptions={detailed_descriptions},
    tags="{tags}",
    HTML_web_color_name="{HTML_web_color_name}",
)
    """

    # 添加全局描述
    global_description = data.pop("0")
    python_code = python_code.format(
        description=global_description["description"],
        detailed_descriptions=global_description["detailed_descriptions"],
        tags=global_description["tags"],
        HTML_web_color_name=global_description["HTML_web_color_name"]
    )

    # 添加局部描述
    for key, value in data.items():
        local_description = f"""
# Set a local description for the canvas
canvas.add_local_description(
    location="{value.get("location", "")}",
    offset="{value.get("offset", "")}",
    area="{value.get("area", "")}",
    distance_to_viewer={value.get("distance_to_viewer", 1.0)},
    description="{value["description"]}",
    detailed_descriptions={value["detailed_descriptions"]},
    tags="{value["tags"]}",
    atmosphere="{value.get("atmosphere", "")}",
    style="{value.get("style", "")}",
    quality_meta="{value.get("quality_meta", "")}",
    HTML_web_color_name="{value["HTML_web_color_name"]}",
)
    """
        python_code += local_description
    start="""
```python

    """
    end="\n\n```"
    return start+python_code+end

class omost_json2py:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"omost_json": ("STRING", {"multiline": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("omost_py",)

    FUNCTION = "convert_txt2json"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def convert_txt2json(self, omost_json):
        omost_py=json_to_py(omost_json)
        return (omost_py,)


NODE_CLASS_MAPPINGS = {"omost_json2py": omost_json2py}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"omost_json2py": "omost JSON转Python"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"omost_json2py": "omost json2py"}