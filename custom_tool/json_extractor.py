import json
import re
import ast
import locale
from json_repair import repair_json

def try_parse_ast_to_json(function_string: str) -> tuple[str, dict]:
    """
     # 示例函数字符串
    function_string = "tool_call(first_int={'title': 'First Int', 'type': 'integer'}, second_int={'title': 'Second Int', 'type': 'integer'})"
    :return:
    """

    tree = ast.parse(str(function_string).strip())
    ast_info = ""
    json_result = {}
    # 查找函数调用节点并提取信息
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            function_name = node.func.id
            args = {kw.arg: kw.value for kw in node.keywords}
            ast_info += f"Function Name: {function_name}\r\n"
            for arg, value in args.items():
                ast_info += f"Argument Name: {arg}\n"
                ast_info += f"Argument Value: {ast.dump(value)}\n"
                json_result[arg] = ast.literal_eval(value)

    return ast_info, json_result


class json_extractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":  {
                "input": ("STRING", {"forceInput": True}),
                "is_enable": ("BOOLEAN", {"default": True}),
                }
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)
    FUNCTION = "json_extract"

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def json_extract(self, input, is_enable=True):
        
        """JSON cleaning and formatting utilities."""
        # Sometimes, the LLM returns a json string with some extra description, this function will clean it up.
        if is_enable == False:
            return (None,)
        
        result = None
        try:
            # Try parse first
            result = json.loads(input)
        except json.JSONDecodeError:
            print("Warning: Error decoding faulty json, attempting repair")

        _pattern = r"\{(.*)\}"
        _match = re.search(_pattern, input)
        input = "{" + _match.group(1) + "}" if _match else input

        # Clean up json string.
        input = (
            input.replace("{{", "{")
            .replace("}}", "}")
            .replace('"[{', "[{")
            .replace('}]"', "}]")
            .replace("\\", " ")
            .replace("\\n", " ")
            .replace("\n", " ")
            .replace("\r", "")
            .strip()
        )

        # Remove JSON Markdown Frame
        if input.startswith("```json"):
            input = input[len("```json"):]
        if input.startswith("```"):
            input = input[len("```"):]
        if input.endswith("```"):
            input = input[: len(input) - len("```")]
        print("input=%s", input)
        try:
            result = json.loads(input)
            result = json.dumps(result, ensure_ascii=False, indent=4)
            return (result,)
        except json.JSONDecodeError:
            # Fixup potentially malformed json string using json_repair.
            
            json_info = str(repair_json(json_str=input, return_objects=False))

            # Generate JSON-string output using best-attempt prompting & parsing techniques.
            try:

                if len(json_info) < len(input):
                    json_info, result = try_parse_ast_to_json(input)
                else:
                    result = json.loads(json_info)

            except json.JSONDecodeError:
                print("error loading json, json=%s", input)
                return ("error loading json",)
            else:
                if not isinstance(result, dict):
                    print("not expected dict type. type=%s:", type(result))
                    return ("not expected dict type. type=%s:", type(result),)
                result = json.dumps(result, ensure_ascii=False, indent=4)
                return (result,)
        

NODE_CLASS_MAPPINGS = {
    "json_extractor": json_extractor,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
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
    NODE_DISPLAY_NAME_MAPPINGS = {"json_extractor": "JSON提取器🐶"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"json_extractor": "JSON Repair🐶"}