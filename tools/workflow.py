import datetime
import hashlib
import io
import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid

import numpy as np
import pandas as pd
import pygments
import streamlit as st
import torch
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from PIL import Image, ImageOps, ImageSequence
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from ..config import current_dir_path

server_address = "127.0.0.1:8190"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


def get_all(ws, prompt):
    prompt_id = queue_prompt(prompt)["prompt_id"]
    output_images = {}
    output_text = ""
    while True:
        try:
            history = get_history(prompt_id)[prompt_id]
            break
        except Exception:
            time.sleep(0.1)
            continue
    for o in history["outputs"]:
        for node_id in history["outputs"]:
            node_output = history["outputs"][node_id]
            if "images" in node_output:
                images_output = []
                for image in node_output["images"]:
                    image_data = get_image(image["filename"], image["subfolder"], image["type"])
                    images_output.append(image_data)
                output_images[node_id] = images_output
            if "response" in node_output:
                output_text = node_output["response"][0]["content"]

    return output_images, output_text


def api(
    file_content="",
    file_path="",
    img_path1="",
    img_path2="",
    system_prompt="你是一个强大的智能助手",
    user_prompt="",
    positive_prompt="",
    negative_prompt="",
    model_name="",
    workflow_path="测试画画app.json",
):
    global current_dir_path
    workflow_path = workflow_path
    WF_path = os.path.join(current_dir_path, "workflow_api", workflow_path)
    with open(WF_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)

    for p in prompt:
        # 如果p的class_type是start_workflow
        if prompt[p]["class_type"] == "start_workflow":
            if file_content != "":
                prompt[p]["inputs"]["file_content"] = file_content
            prompt[p]["inputs"]["file_path"] = file_path
            prompt[p]["inputs"]["img_path1"] = img_path1
            prompt[p]["inputs"]["img_path2"] = img_path2
            prompt[p]["inputs"]["system_prompt"] = system_prompt
            prompt[p]["inputs"]["user_prompt"] = user_prompt
            prompt[p]["inputs"]["positive_prompt"] = positive_prompt
            prompt[p]["inputs"]["negative_prompt"] = negative_prompt
            prompt[p]["inputs"]["model_name"] = model_name

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images, res = get_all(ws, prompt)
    return images, res


def check_port_and_execute_bat(port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", port))
    if result != 0:
        print(f"端口 {port} 未被占用，正在执行命令...")
        if platform.system() == "Windows" or platform.system() == "Darwin":
            subprocess.Popen(command, shell=True)
        else:
            subprocess.Popen(command)
        while True:
            result = sock.connect_ex(("localhost", port))
            if result == 0:
                print(f"端口 {port} 已经开放，可以正常访问。")
                sock.close()
                break
            else:
                print(f"端口 {port} 未开放，等待中...")
                time.sleep(1)  # 等待1秒后再次检查端口状态
    else:
        print(f"端口 {port} 已被占用。")
    sock.close()


api_path = os.path.join(current_dir_path, "workflow_api")
# 获取apipath文件夹下的所有json文件名
json_files = [f for f in os.listdir(api_path) if f.endswith(".json")]


def execute_command_in_new_window(interpreter, root_path, port):
    os_type = platform.system()
    command = ""

    if os_type == "Windows":
        command = f'start cmd /k "{interpreter} {root_path} --port {port}"'
    elif os_type == "Darwin":  # 'Darwin' 是 macOS 的系统类型
        # 使用 AppleScript 打开新的 Terminal 窗口
        command = f'osascript -e \'tell application "Terminal" to do script "{interpreter} {root_path} --port {port}"\''
    else:
        # 对于 Linux，检查 'screen' 或 'tmux'
        try:
            command = ["screen", "-dmS", "mysession", interpreter, root_path, "--port", str(port)]
        except FileNotFoundError:
            try:
                command = ["tmux", "new-session", "-d", interpreter, root_path, "--port", str(port)]
            except FileNotFoundError:
                print("错误：未找到合适的终端复用器。请安装 screen 或 tmux。")
                return
    check_port_and_execute_bat(port, command)


class workflow_transfer:
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "file_path": ("STRING", {}),
                "img_path1": ("STRING", {}),
                "img_path2": ("STRING", {}),
                "system_prompt": ("STRING", {}),
                "user_prompt": ("STRING", {}),
                "positive_prompt": ("STRING", {}),
                "negative_prompt": ("STRING", {}),
                "model_name": ("STRING", {}),
                "workflow_path": (json_files, {}),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "STRING",
    )
    RETURN_NAMES = (
        "images",
        "text",
    )

    FUNCTION = "transfer"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def transfer(
        self,
        file_content="",
        file_path="",
        img_path1="",
        img_path2="",
        system_prompt="你是一个强大的智能助手",
        user_prompt="",
        positive_prompt="",
        negative_prompt="",
        model_name="",
        workflow_path="测试画画app.json",
        is_enable=True,
    ):
        if is_enable == False:
            return (None,)
        # 获取当前Python解释器的路径
        interpreter = sys.executable

        # 获取main.py的绝对路径
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "main.py"))

        execute_command_in_new_window(interpreter, root_path, 8190)

        output_images, output_text = api(
            file_content,
            file_path,
            img_path1,
            img_path2,
            system_prompt,
            user_prompt,
            positive_prompt,
            negative_prompt,
            model_name,
            workflow_path,
        )
        img_out = []
        if output_images == {}:
            output_images = None
        elif output_images is not None:
            for node_id in output_images:
                for image_data in output_images[node_id]:
                    img = Image.open(io.BytesIO(image_data))
                    img = ImageOps.exif_transpose(img)
                    if img.mode == "I":
                        img = img.point(lambda i: i * (1 / 256)).convert("L")
                    image = img.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image).unsqueeze(0)
                    img_out.append(image)
        if len(img_out) > 1:
            img_out = torch.cat(img_out, dim=0)
        elif img_out:
            img_out = img_out[0]
        if output_text == "":
            output_text = None
        return (
            img_out,
            output_text,
        )
    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value

class workflow_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "workflow_name": ("STRING", {"multiline": True, "default": "写诗.json,draw.json"}),
                "workflow_description": ("STRING", {"multiline": True, "default": "写诗.json是一个根据用户输入的信息生成诗歌的工具，draw.json is a tool that generates images based on user prompt."}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "workflow"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"

    def workflow(self, workflow_name,workflow_description, is_enable="enable"):
        if is_enable == "disable":
            return (None,)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "work_flow",
                    "description": "这是一个根据workflow_name调用workflow的工具，请根据workflow_name判断这个工作流的作用，然后调用对应的工作流",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "workflow_name": {
                                "type": "string",
                                "description": f"请从[{str(workflow_name)}]中选择json文件名作为要调用的workflow_name。这些工作流分别的使用说明为：{workflow_description}。该参数用于指定要调用的workflow文件名，是一个带.json后缀名的文件名。",
                            },
                            "user_prompt": {
                                "type": "string",
                                "description": "用户输入的信息",
                            },
                        },
                        "required": ["workflow_name","user_prompt"]
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


def work_flow(
    user_prompt="",
    workflow_name="测试画画app.json",
):
    # 用re去掉workflow_name字符串中的'['、']'字符
    workflow_name = re.sub(r"[\[\]]", "", workflow_name)

    # 获取当前Python解释器的路径
    interpreter = sys.executable

    # 获取main.py的绝对路径
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "main.py"))

    execute_command_in_new_window(interpreter, root_path, 8190)
    global current_dir_path
    WF_path = os.path.join(current_dir_path, "workflow_api", workflow_name)
    with open(WF_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)

    for p in prompt:
        # 如果p的class_type是start_workflow
        if prompt[p]["class_type"] == "start_workflow":
            prompt[p]["inputs"]["user_prompt"] = user_prompt

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images, res = get_all(ws, prompt)
    img_out = []
    if images == {}:
        images = None
    elif images is not None:
        for node_id in images:
            for image_data in images[node_id]:
                img = Image.open(io.BytesIO(image_data))
                img = ImageOps.exif_transpose(img)
                if img.mode == "I":
                    img = img.point(lambda i: i * (1 / 256)).convert("L")
                image = img.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image).unsqueeze(0)
                img_out.append(image)
    if len(img_out) > 1:
        img_out = torch.cat(img_out, dim=0)
    elif img_out:
        img_out = img_out[0]
    return res, img_out
