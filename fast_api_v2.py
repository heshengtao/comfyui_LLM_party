# 更新后的 fast_api_v2.py 内容
import argparse
import atexit
import base64
import configparser
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import uuid
from io import BytesIO
from typing import Any, List, Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
import numpy as np
import requests
import torch
import websocket
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps
from pydantic import BaseModel

current_dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(current_dir_path, "config.ini"))
# 获取配置文件中的参数
fastapi_api_key = config.get("API_KEYS", "fastapi_api_key", fallback="")
client_id = str(uuid.uuid4())
import uvicorn
import asyncio
import subprocess
import logging

parser = argparse.ArgumentParser(description="Run the server with specified host and port.")
parser.add_argument("--port", type=str, default=8188, help="Server address to connect to.")
args = parser.parse_args()
server_address = f"127.0.0.1:{args.port}"
# 默认的端口是server_address的端口+10000
fastapi_port = int(args.port) + 10000

# current_dir_path上两级目录下的main.py文件
main_path = os.path.join(current_dir_path, "..", "..", "main.py")

# 全局变量来存储ComfyUI进程
comfyui_process = None

def cleanup():
    global comfyui_process
    if comfyui_process:
        logging.info("正在关闭ComfyUI进程...")
        comfyui_process.terminate()
        try:
            comfyui_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            comfyui_process.kill()
        logging.info("ComfyUI进程已关闭")

# 注册清理函数
atexit.register(cleanup)

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

def get_all(prompt):
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

def api(file_content="", image_input=None, file_path="", img_path="", system_prompt="你是一个强大的智能助手", user_prompt="", positive_prompt="", negative_prompt="", model_name="", workflow_path="测试画画api.json", user_history=""):
    global current_dir_path
    workflow_path = workflow_path
    WF_path = os.path.join(current_dir_path, "workflow_api", workflow_path)
    # 判断 WF_path 是否存在
    if not os.path.exists(WF_path):
        raise HTTPException(status_code=404, detail="Workflow file not found")
    with open(WF_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt = json.loads(prompt_text)

    for p in prompt:
        # 如果p的class_type是start_workflow
        if prompt[p]["class_type"] == "start_workflow":
            if file_content != "":
                prompt[p]["inputs"]["file_content"] = file_content
            if image_input is not None and image_input != []:
                prompt[p]["inputs"]["image_input"] = image_input
            prompt[p]["inputs"]["file_path"] = file_path
            prompt[p]["inputs"]["img_path1"] = img_path
            prompt[p]["inputs"]["system_prompt"] = system_prompt
            prompt[p]["inputs"]["user_prompt"] = user_prompt
            prompt[p]["inputs"]["positive_prompt"] = positive_prompt
            prompt[p]["inputs"]["negative_prompt"] = negative_prompt
            prompt[p]["inputs"]["model_name"] = model_name
            prompt[p]["inputs"]["user_history"] = user_history

    images, res = get_all(prompt)
    return images, res

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: Any

class CompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int = 150
    stream: bool = False

VALID_API_KEY = fastapi_api_key

security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    不进行实际的API密钥验证，允许任何API密钥通过。
    """
    # 这里可以选择性地添加一些日志记录或其他处理逻辑
    return credentials.credentials

@app.get("/v1/models")
async def get_models():
    try:
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        workflow_api_path = os.path.join(current_dir_path, "workflow_api")

        model_names = [
            os.path.splitext(file)[0]
            for file in os.listdir(workflow_api_path)
            if file.endswith(".json")
        ]

        response = {
            "data": [
                {
                    "id": model_name,
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "comfyui-LLM-party",
                    "permission": []
                }
                for model_name in model_names
            ],
            "object": "list"
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_response(response_text: str, model_name: str):
    chunks = []
    current_chunk = []
    # 如果response_text包含中文字符
    if re.search(r'[\u4e00-\u9fa5]', response_text):
        # 定义一个包含中文标点符号的正则表达式模式
        punctuation_pattern = r'[，。；：！？\s]'

        # 使用正则表达式进行分割，但是保留标点符号
        words = re.split(punctuation_pattern, response_text)
        words = [word + punct for word, punct in zip(words, re.findall(punctuation_pattern, response_text) + ['']) if word]
    else:
        # 定义一个包含英文标点符号的正则表达式模式
        punctuation_pattern = r'[.,;:!?\s]'
        # 使用正则表达式进行分割，但是保留标点符号
        words = re.split(punctuation_pattern, response_text)
        words = [word + punct for word, punct in zip(words, re.findall(punctuation_pattern, response_text) + ['']) if word]
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= 1:  # Send 3 words at a time
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:  # Add any remaining words
        chunks.append(" ".join(current_chunk))

    for i, chunk in enumerate(chunks):
        response_chunk = {
            "id": "chatcmpl-" + str(uuid.uuid4()),
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model_name,
            "choices": [
                {
                    "delta": {
                        "role": "assistant" if i == 0 else None,
                        "content": chunk
                    },
                    "index": 0,
                    "finish_reason": "stop" if i == len(chunks) - 1 else None
                }
            ]
        }
        yield f"data: {json.dumps(response_chunk)}\n\n"
        await asyncio.sleep(0.1)  # Add small delay between chunks

    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def create_completion(request_data: CompletionRequest, dependency=Depends(verify_api_key)):
    try:
        if request_data.stream:
            response = await process_request(request_data)
            if isinstance(response, dict) and "choices" in response:
                content = response["choices"][0]["message"]["content"]
                return StreamingResponse(
                    stream_response(content, request_data.model),
                    media_type="text/event-stream"
                )
        else:
            response = await process_request(request_data)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_request(request_data: CompletionRequest):
    model_name = request_data.model
    print(model_name)
    base64_encoded_list = []
    system_prompt = ""
    user_histories = []
    for message in request_data.messages:
        user_histories.append({"role": message.role, "content": message.content})
    msg = request_data.messages[-1]
    if isinstance(msg.content, str):
        if msg.role == "system":
            system_prompt = msg.content
        elif msg.role == "user":
            user_prompt = msg.content
    elif isinstance(msg.content, list):
        for content in msg.content:
            if isinstance(content, dict) and "type" in content:
                if content["type"] == "text":
                    user_prompt = content["text"]
                elif content["type"] == "image_url":
                    if isinstance(content["image_url"], str):
                        if content["image_url"].startswith("data:image/png;base64,"):
                            base64_data = content["image_url"].split("data:image/png;base64,")[1]
                            base64_encoded_list.append(base64_data)
                        # 如果是本地文件路径
                        elif os.path.isfile(content["image_url"]):
                            with open(content["image_url"], "rb") as image_file:
                                base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
                        else:
                            # allowed_domains包含你所有的可信域名
                            # allowed_domains = ["trusteddomain.com", "anothertrusteddomain.com"]
                            # parsed_url = urllib.parse.urlparse(content["image_url"])
                            # if parsed_url.netloc not in allowed_domains:
                            #     raise HTTPException(status_code=400, detail="Image URL domain is not allowed.")
                            async with httpx.AsyncClient() as client:
                                response = await client.get(content["image_url"])
                                if response.status_code == 200:
                                    image_bytes = BytesIO(response.content)
                                    base64_encoded = base64.b64encode(image_bytes.read()).decode("utf-8")
                                    base64_encoded_list.append(base64_encoded)
                                else:
                                    raise HTTPException(status_code=400, detail="Image could not be retrieved.")

    img_out = []
    for base64_encoded in base64_encoded_list:
        image_bytes = BytesIO(base64.b64decode(base64_encoded))
        img = Image.open(image_bytes)
        img = ImageOps.exif_transpose(img)

        if img.mode == "I":
            img = img.point(lambda i: i * (1 / 256)).convert("L")

        img = img.convert("RGB")
        image_np = np.array(img).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np).permute(2, 0, 1).unsqueeze(0)
        img_out.append(image_tensor)

    workflow_path = model_name + ".json"
    user_histories = json.dumps(user_histories, ensure_ascii=False)
    images, response = api(
        "",
        img_out,
        "",
        "",
        system_prompt,
        user_prompt,
        "",
        "",
        "",
        workflow_path,
        user_histories,
    )
    all_response = {"text":"", "image_urls":[],"audio_url":"","vedio_url":""}
    if images is not None or images != []:
        base64_images = []

        for node_id in images:
            for image_data in images[node_id]:
                img_base64 = base64.b64encode(image_data).decode("utf-8")

            config_path = os.path.join(current_dir_path, "config.ini")
            config = configparser.ConfigParser()
            config.read(config_path, encoding="utf-8")
            api_keys = {}
            if "API_KEYS" in config:
                api_keys = config["API_KEYS"]

            imgbb_key = api_keys.get("imgbb_api")
            print(imgbb_key)

            if imgbb_key is None or imgbb_key == "":
                # 把img_base64保存到当前目录下的output文件夹
                output_dir = os.path.join(current_dir_path, "output")
                os.makedirs(output_dir, exist_ok=True)
                # 时间戳
                timestamp = int(time.time())
                filename = os.path.join(output_dir, f"{timestamp}.png")
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(img_base64))
                base64_images.append(filename)
            else:
                url = "https://api.imgbb.com/1/upload"
                payload = {"key": imgbb_key, "image": img_base64}
                response0 = requests.post(url, data=payload)
                if response0.status_code == 200:
                    result = response0.json()
                    img_url = result["data"]["url"]
                else:
                    return "Error: " + response0.text
                print(img_url)
                base64_images.append(img_url)

        all_response["image_urls"]= base64_images
    elif response is not None:
        all_response["text"]= response
    response_data = {
        "id": "0",
        "object": "text_completion",
        "created": int(time.time()),
        "model": model_name,
        "system_fingerprint": "fp_0",
        "choices": [
            {
                "message": {"role": "assistant", "content": all_response},
                "index": 0,
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 10},
    }

    return response_data

async def start_comfyui_server():
    # 构建启动 ComfyUI 的命令
    comfyui_cmd = [
        sys.executable,
        "-s",
        main_path,
        "--port",
        str(args.port)
    ]

    global comfyui_process
    try:
        comfyui_process = subprocess.Popen(comfyui_cmd, cwd=os.path.dirname(main_path))
        logging.info(f"ComfyUI 服务器已在 {server_address} 启动")
    except Exception as e:
        logging.error(f"启动ComfyUI服务器时发生错误: {e}")

async def run_server():
    await start_comfyui_server()
    config = uvicorn.Config(app, host="127.0.0.1", port=fastapi_port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(run_server())
