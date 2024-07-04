import json

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
        with open(file_path, 'r', encoding='utf-8') as data:
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
        return (output)

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
        "STRING",
    )
    RETURN_NAMES = (
        "show_json_file",
        "value_by_key",
    )
    OUTPUT_NODE = True
    FUNCTION = "json_parser_tool"

    CATEGORY = "大模型派对（llm_party）/函数（function）"
    
    def json_parser_tool(self, file_path: str, key=None, is_enable=True):
        if is_enable == False:
            return (None,)
        data_json = json_loader(file_path)
        if key == None:
            return (data_json, None, )
        data_dict = json.loads(data_json)
        try:
            value = data_dict[key]
        except KeyError:
            print(f"Key '{key}' not found in JSON data.")
            value = None
        out = json.dumps(value, ensure_ascii=False)
        return (data_json, out,)

class json_get_value:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"default": ""}),
                "key": ("STRING", {}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("content",)
    FUNCTION = "get_value"
    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def get_value(self, text, key = None, is_enable=True):
        if is_enable == False:
            return (None,)
        try:
            data = json.loads(text)
            out = data[key]
            return (out,)
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return (None,)

# _TOOL_HOOKS = ["json_parser"]    
NODE_CLASS_MAPPINGS = {
    "json_parser":json_parser, 
    "json_get_value":json_get_value,
    }
NODE_DISPLAY_NAME_MAPPINGS = {
    "json_parser":"JSON文件解析🐶（json_parser）",
    "json_get_value":"JSON取值🐶（json_get_value）",}

# if __name__ == "__main__":
#     file_path_ = "E:\\project\\comfyui_LLM_party\\file\\量子永生教.json"
#     key_ = "0"
#     json_content, out = json_parser.json_parser_tool(file_path = file_path_, key = key_)
#     print(json_content)
#     print(out)
#     value = json_get_value.get_value(out, "story")
#     print(value)