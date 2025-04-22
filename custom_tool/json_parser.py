import json
import locale


def load_json_file(file_path) -> dict:
    def set_to_list(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: set_to_list(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [set_to_list(element) for element in obj]
        else:
            return obj

    try:
        with open(file_path, "r", encoding="utf-8") as data:
            data = json.load(data)
            data = set_to_list(data)
            return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None


def json_loader(file_path: str, is_enable=True) -> str:
    if is_enable == False:
        return (None,)
    output = load_json_file(file_path)
    output = json.dumps(output, ensure_ascii=False)
    return output
class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class json_parser:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": "data.json"}),
                "key": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (
        "STRING",
        any_type,
    )
    RETURN_NAMES = (
        "show_json_file",
        "value_by_key",
    )
    OUTPUT_NODE = True
    FUNCTION = "json_parser_tool"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def json_parser_tool(self, file_path: str, key=None, is_enable=True):
        if is_enable == False:
            return (None,)
        data_json = json_loader(file_path)
        if key == None:
            return (
                data_json,
                None,
            )
        data_dict = json.loads(data_json)
        try:
            value = data_dict[key]
        except KeyError:
            print(f"Key '{key}' not found in JSON data.")
            value = None
        return (
            data_json,
            value,
        )



class json_get_value:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "key": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("any",)
    FUNCTION = "get_value"
    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def get_value(self, text, key=None, is_enable=True):
        if is_enable == False:
            return (None,)
        try:
            data = json.loads(text)
            try:
                if isinstance(data, dict):
                    out = data[key]
                elif isinstance(data, list):
                    out = data[int(key)]
            except (KeyError, IndexError, ValueError):
                return (None,)
            # 判断是否为列表或者是字典
            if isinstance(out, list) or isinstance(out, dict):
                out = json.dumps(out, ensure_ascii=False, indent=4)
                return (out.strip(),)
            else:
                return (out,)
            
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return (None,)


# _TOOL_HOOKS = ["json_parser"]
NODE_CLASS_MAPPINGS = {
    "json_parser": json_parser,
    "json_get_value": json_get_value,
}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"json_parser": "JSON文件解析🐶", "json_get_value": "JSON取值🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"json_parser": "JSON File Parser🐶", "json_get_value": "JSON Get Value🐶"}


# if __name__ == "__main__":
#     file_path_ = "E:\\project\\comfyui_LLM_party\\file\\量子永生教.json"
#     key_ = "0"
#     json_content, out = json_parser.json_parser_tool(file_path = file_path_, key = key_)
#     print(json_content)
#     print(out)
#     value = json_get_value.get_value(out, "story")
#     print(value)
