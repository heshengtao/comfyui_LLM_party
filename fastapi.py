import configparser
import time

import openai
import requests
from fastapi import FastAPI, HTTPException,Request, Depends
from pydantic import BaseModel, validator
from typing import Any, List, Union, Optional
import httpx
import base64
from io import BytesIO
from PIL import Image, ImageOps
import numpy as np
import torch
import os

import json
import urllib.parse
import urllib.request
import uuid

import pandas as pd
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from PIL import Image
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
current_dir_path = os.path.dirname(os.path.realpath(__file__))
server_address = "127.0.0.1:8188"
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
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
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
    image_input=None,
    file_path="",
    img_path="",
    system_prompt="你是一个强大的智能助手",
    user_prompt="",
    positive_prompt="",
    negative_prompt="",
    model_name="",
    workflow_path="测试画画api.json",
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
            if image_input is not None and image_input!=[]:
                prompt[p]["inputs"]["image_input"] = image_input
            prompt[p]["inputs"]["file_path"] = file_path
            prompt[p]["inputs"]["img_path"] = img_path
            prompt[p]["inputs"]["system_prompt"] = system_prompt
            prompt[p]["inputs"]["user_prompt"] = user_prompt
            prompt[p]["inputs"]["positive_prompt"] = positive_prompt
            prompt[p]["inputs"]["negative_prompt"] = negative_prompt
            prompt[p]["inputs"]["model_name"] = model_name

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images, res = get_all(ws, prompt)
    return images, res


app = FastAPI()
# 定义请求中的消息内容
class MessageContent(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[Union[str, dict]] = None

    # 自定义验证器来处理image_url字段
    @validator('image_url', pre=True)
    def parse_image_url(cls, value):
        if isinstance(value, dict) and 'url' in value:
            return value['url']
        return value

# 定义请求中的消息
class Message(BaseModel):
    role: str
    content: Any

# 定义整个请求体
class CompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int

# 中间件或依赖项来验证 API 密钥
async def verify_api_key(request: Request):
    # 从请求头中获取 API 密钥
    api_key = request.headers.get("Authorization").split("Bearer ")[-1]


# 创建路由处理函数
@app.post("/v1/chat/completions")
async def create_completion(request_data: CompletionRequest):
    # 这里可以添加您的处理逻辑
    # 例如，解析文本和图片URL，并生成相应的响应
    try:
        # 处理请求并生成响应
        response = await process_request(request_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 返回生成的响应
    return response

# 异步函数来处理请求并生成响应
async def process_request(request_data: CompletionRequest,dependency=Depends(verify_api_key)):
    model_name = request_data.model

    base64_encoded_list=[]
    # 遍历消息
    for message in request_data.messages:
        # 检查 content 是否为字符串
        if isinstance(message.content, str):
            user_prompt = message.content
        # 如果 content 是列表，按原有逻辑处理
        elif isinstance(message.content, list):
            for content in message.content:
                if content.type == "text":
                    # 处理文本
                    user_prompt = content.text
                elif content.type == "image_url":
                    if isinstance(content.image_url, str):
                        # 检查URL是否为Base64编码的数据URI
                        if content.image_url.startswith('data:image/jpeg;base64,'):
                            # 提取Base64编码的图片数据
                            base64_data = content.image_url.split('data:image/jpeg;base64,')[1]
                            base64_encoded_list.append(base64_data)
                        else:
                            # 下载图片并转换为Base64编码
                            async with httpx.AsyncClient() as client:
                                response = await client.get(content.image_url)
                                if response.status_code == 200:
                                    image_bytes = BytesIO(response.content)
                                    base64_encoded = base64.b64encode(image_bytes.read()).decode('utf-8')
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

        # 将图像转换为RGB
        img = img.convert("RGB")

        # 将图像转换为numpy数组，并归一化
        image_np = np.array(img).astype(np.float32) / 255.0

        # 将numpy数组转换为PyTorch张量
        image_tensor = torch.from_numpy(image_np).permute(2, 0, 1).unsqueeze(0)

        # 添加到输出列表
        img_out.append(image_tensor)
    
    workflow_path = model_name + ".json"
    # 调用API函数
    images, response = api(
        "",
        img_out,
        "",
        "",
        "",
        user_prompt,
        "",
        "",
        "",
        workflow_path,
    )
    if images is None or images==[]:
        # 构建响应数据
        response_data = {
            "id": "0",
            "object": "text_completion",
            "created": int(time.time()),  # 实时时间戳
            "model": model_name,
            "system_fingerprint": "fp_0",
            "choices": [
                {
                    "message": {"content": response},
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "Stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    else:
        base64_images = []  # 用于存储Base64编码的图像字符串

        for image_tensor in img_out:
            # 将张量转换为PIL图像
            image_np = image_tensor.squeeze(0).permute(1, 2, 0).numpy()
            image_np = (image_np * 255).astype(np.uint8)
            img = Image.fromarray(image_np)

            # 将PIL图像保存到字节流中
            buffer = BytesIO()
            img.save(buffer, format="JPEG")  # 您可以根据需要更改图像格式
            buffer.seek(0)

            # 将字节流编码为Base64
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            # 构建config.ini的绝对路径
            config_path = os.path.join(current_dir_path, "config.ini")
            #从config.ini找到imgbb_key
            config = configparser.ConfigParser()
            config.read(config_path, encoding="utf-8")
            api_keys = {}
            if "API_KEYS" in config:
                api_keys = config["API_KEYS"]

            imgbb_key=api_keys.get("imgbb_api")

            if imgbb_key is None or imgbb_key=="":
                #返回imgbb_key缺失，需要在config.ini填入的报错
                return {
                    "error": "imgbb_api key is missing in config.ini"
                }

            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_key, "image": img_base64}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
            else:
                return "Error: " + response.text
            base64_images.append(img_url)

        for img in base64_images:
            response_url=f"![image]({img})"
            response += "\n"+response_url+"\n"

        # 构建响应数据
        response_data = {
            "id": "0",
            "object": "text_completion",
            "created": int(time.time()),  # 实时时间戳
            "model": model_name,
            "system_fingerprint": "fp_0",
            "choices": [
                {
                    "message": {
                        "content": response,
                        },
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "Stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8817)


