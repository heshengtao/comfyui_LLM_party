import configparser
import os
import openai
import server
from aiohttp import web
from .config import load_api_keys
import subprocess
import sys
import asyncio
import shlex

# Assuming this file is in the same directory as your custom nodes
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
llm_api_keys = load_api_keys(config_path)
llm_api_key=llm_api_keys.get("openai_api_key").strip()
llm_base_url=llm_api_keys.get("base_url").strip()
if llm_api_key == "" or llm_api_key =="sk-XXXXX" or llm_base_url == "":
    models_dict =[]
else:
    try:
        client = openai.OpenAI(api_key=llm_api_key, base_url=llm_base_url)
        models_response = client.models.list()
        models_dict = [model.id for model in models_response.data]
        openai.api_key=llm_api_key
        openai.base_url=llm_base_url
    except Exception as e:
        models_dict = []
        print(e)

# 全局变量来跟踪FastAPI服务器的状态
fastapi_process = None

@server.PromptServer.instance.routes.post('/party/update_config')
async def update_config(request):
    try:
        data = await request.json()
        config = configparser.ConfigParser()
        config.read(config_path)

        if 'API_KEYS' not in config:
            config['API_KEYS'] = {}

        config['API_KEYS']['openai_api_key'] = data['openai_api_key']
        config['API_KEYS']['base_url'] = data['base_url']

        with open(config_path, 'w') as configfile:
            config.write(configfile)
        llm_api_keys = load_api_keys(config_path)
        llm_api_key=llm_api_keys.get("openai_api_key").strip()
        llm_base_url=llm_api_keys.get("base_url").strip()
        global models_dict
        if llm_api_key == "" or llm_api_key =="sk-XXXXX" or llm_base_url == "":
            models_dict =[]
        else:
            try:
                client = openai.OpenAI(api_key=llm_api_key, base_url=llm_base_url)
                models_response = client.models.list()
                models_dict = [model.id for model in models_response.data]
                openai.api_key=llm_api_key
                openai.base_url=llm_base_url
            except Exception as e:
                models_dict = []
                print(e)
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

def start_fastapi_server(fast_api_path):
    cmd = f"{sys.executable} {fast_api_path} --host 127.0.0.1 --port 8187"
    if sys.platform == 'win32':
        return subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif sys.platform == 'darwin':  # macOS
        return subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{cmd}"'])
    else:  # Linux
        try:
            # 检查 screen 是否可用
            subprocess.run(['which', 'screen'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 使用 screen 启动 FastAPI 服务器
            screen_name = "fastapi_server"
            full_cmd = f"screen -dmS {screen_name} bash -c '{cmd}'"
            subprocess.run(full_cmd, shell=True, check=True)
            return subprocess.Popen(['echo', 'FastAPI server started in screen session'])
        except subprocess.CalledProcessError:
            print("Error: 'screen' command not found. Please install screen or use an alternative method.")
            return None

@server.PromptServer.instance.routes.post('/party/fastapi')
async def start_fast_api(request):
    global fastapi_process
    try:
        if fastapi_process is not None and fastapi_process.poll() is None:
            # FastAPI 服务器已经在运行
            return web.json_response({"status": "success", "message": "FastAPI服务已经在运行"})

        # 获取当前文件的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建fast_api.py的完整路径
        fast_api_path = os.path.join(current_dir, 'fast_api.py')
        
        # 启动FastAPI服务器
        fastapi_process = start_fastapi_server(fast_api_path)
        
        if fastapi_process is None:
            return web.json_response({"status": "error", "message": "无法启动FastAPI服务器"}, status=500)
        
        # 等待一段时间，确保服务器有时间启动
        await asyncio.sleep(5)
        
        if sys.platform != 'win32' and sys.platform != 'darwin':
            # 对于Linux，我们假设服务器已经在screen会话中启动
            return web.json_response({"status": "success", "message": "FastAPI服务已在screen会话中启动"})
        elif fastapi_process.poll() is None:
            return web.json_response({"status": "success", "message": "FastAPI服务已启动"})
        else:
            error_message = "FastAPI启动失败"
            return web.json_response({"status": "error", "message": error_message}, status=500)
    
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)
