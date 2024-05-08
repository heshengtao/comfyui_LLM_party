import json
import re
import subprocess
import sys
import os
from contextlib import redirect_stdout
import io
import virtualenv

def create_virtual_env(env_name, path='.'):
    print("Creating virtual environment...")
    env_path = os.path.join(path, env_name)
    try:
        if not os.path.isdir(env_path):
            virtualenv.cli_run([env_path])
            print("Virtual environment created successfully.")
        else:
            print("Virtual environment already exists.")
    except Exception as e:
        print(f"Error creating virtual environment: {e}")

def activate_virtual_env(env_name):
    print("Activating virtual environment...")
    try:
        if sys.platform == "win32":
            activate_script = os.path.join(env_name, 'Scripts', 'activate')
        else:
            activate_script = os.path.join(env_name, 'bin', 'activate')
        subprocess.check_call(activate_script, shell=True)
        print("Virtual environment activated successfully.")
    except Exception as e:
        print(f"Error activating virtual environment: {e}")

def install_package(env_name, package):
    print("Installing package:", package)
    # 使用正确的虚拟环境内的 pip 可执行文件路径
    pip_path = os.path.join(env_name, 'Scripts', 'pip') if sys.platform == "win32" else os.path.join(env_name, 'bin', 'pip')
    subprocess.check_call([pip_path, "install", package])

def execute_code(env_name, code):
    print("Executing code...")
    print(code)
    # 创建一个临时文件来存储代码
    temp_file = os.path.join("aienv", "temp_code.py")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(code)
    # 使用 subprocess.run() 运行临时文件
    if sys.platform == "win32":
        activate_script = os.path.join(env_name, 'Scripts', 'activate')
    else:
        activate_script = os.path.join(env_name, 'bin', 'activate')
    subprocess.check_call(activate_script, shell=True)
    python_path = os.path.join(env_name, 'Scripts', 'python.exe')
    result = subprocess.run([python_path, temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,encoding='utf-8')
    # 获取标准输出
    if result.stdout is not None:
        output = result.stdout.strip()
    else:
        output = None
    err=result.stderr
    print(output+"\n"+str(err))
    if err == '':
        os.remove(temp_file)
        return output
    else:
        missing_modules = []
        # 使用正则表达式查找所有缺失的模块
        matches = re.finditer(r"ModuleNotFoundError: No module named '(\S+)'", err)
        # 遍历所有匹配项并将模块名添加到列表中
        for match in matches:
            missing_modules.append(match.group(1))
        for module in missing_modules:
            if module=='':
                break
            install_package(env_name, module)
        # 再次运行代码
        # 使用 subprocess.run() 运行临时文件
        if sys.platform == "win32":
            activate_script = os.path.join(env_name, 'Scripts', 'activate')
        else:
            activate_script = os.path.join(env_name, 'bin', 'activate')
        subprocess.check_call(activate_script, shell=True)
        python_path = os.path.join(env_name, 'Scripts', 'python.exe')
        result = subprocess.run([python_path, temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 获取标准输出
        output = result.stdout.strip()
        err=result.stderr.strip()
        print(output+"\n"+err)
        # 清理：删除临时文件
        os.remove(temp_file)
        if err == '':
            return output
        else:
            return "代码未执行成功，错误信息为：" + err


def new_interpreter(code_str):
    env_name = 'aienv'
    code_to_run = code_str

    try:
        create_virtual_env(env_name)
        activate_virtual_env(env_name)
        output = execute_code(env_name, code_to_run)
        print(output)
        return "代码执行成功，控制台输出为：" + str(output)+"\n请根据该信息回答用户问题"
    except Exception as e:
        print(f"Error: {e}")
        return "代码未执行成功，错误信息为：" + f"Error: {e}"


class new_interpreter_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {
                    "default": True
                }),  
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "code"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"



    def code(self, is_enable=True):
        if is_enable==False:
            return (None,)        
        output=    [{
        "type": "function",
        "function": {
            "name": "new_interpreter",
            "description": "用于执行你生成的Python代码，并返回代码的在控制台的输出，适用于执行复杂的Python代码。",
            "parameters": {
                "type": "object",
                "properties": {
                    "code_str": {
                        "type": "string",
                        "description": "需要被执行的Python代码"
                    }
                },
                "required": [
                    "code_str"
                ]
            }
        }
    }]
        out=json.dumps(output, ensure_ascii=False)
        return (out,)