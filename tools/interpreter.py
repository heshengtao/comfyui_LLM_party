import json
import sys
from io import StringIO

original_stdout = sys.stdout


def interpreter(code_str, tool=True):
    local_vars = globals().copy()
    try:
        # Redirect stdout to capture console output
        sys.stdout = StringIO()

        # Execute the code or evaluate the expression
        if "print" in code_str or "\n" in code_str:
            exec(code_str, local_vars, local_vars)
        else:
            sys.stdout = original_stdout
            return "代码执行成功，输出结果为：" + str(eval(code_str))

        # Get the captured console output
        console_output = sys.stdout.getvalue()

        # Restore original stdout
        sys.stdout = original_stdout
        defined_variables = {
            key: value
            for key, value in local_vars.items()
            if key not in globals() or (key in globals() and globals()[key] != value)
        }
        if tool == True:
            return "代码执行成功，输出结果为：" + console_output + str(defined_variables)
        else:
            return console_output + str(defined_variables)
    except Exception as e:
        return "代码未执行成功，错误信息为：" + f"Error: {e}"
    finally:
        sys.stdout = original_stdout

def can_serialize(value):
    try:
        json.dumps(value)
        return True
    except:
        return False

def interpreter2(code_str):
    local_vars = globals().copy()
    try:
        # Redirect stdout to capture console output
        sys.stdout = StringIO()

        # Execute the code or evaluate the expression
        if "print" in code_str or "\n" in code_str:
            exec(code_str, local_vars, local_vars)
        else:
            sys.stdout = original_stdout
            return "代码执行成功，输出结果为：" + str(eval(code_str))

        # Get the captured console output
        console_output = sys.stdout.getvalue()

        # Restore original stdout
        sys.stdout = original_stdout
        defined_variables = {
            key: value
            for key, value in local_vars.items()
            if (key not in globals() or (key in globals() and globals()[key] != value)) and can_serialize(value)
        }
        all_output=defined_variables.copy()
        all_output["console_output"]=console_output
        return console_output, json.dumps(defined_variables),json.dumps(all_output)
    except Exception as e:
        return f"Error: {e}",f"Error: {e}",f"Error: {e}"
    finally:
        sys.stdout = original_stdout

class interpreter_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "code"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/实用（Utility）"

    def code(self, is_enable=True):
        if is_enable == False:
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "interpreter",
                    "description": "用于执行你生成的Python代码，并返回代码的执行结果，适用于执行简单的代码",
                    "parameters": {
                        "type": "object",
                        "properties": {"code_str": {"type": "string", "description": "需要被执行的Python代码"}},
                        "required": ["code_str"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class interpreter_function:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "code_str": ("STRING", {"multiline": True, "default": "print('Hello, party!')"}),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("console_output","defined_variables","all_output")

    FUNCTION = "code"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/转换器（converter）"

    def code(self, is_enable=True, code_str="print('Hello, party!')"):
        if is_enable == False:
            return (None,)
        console_output, defined_variables,all_output = interpreter2(code_str)
        # 替换defined_variables中的'为"
        defined_variables = defined_variables.replace("'", '"')
        return (console_output, defined_variables,all_output,)
