import configparser
import logging
import os
import traceback
import openai
import server
from aiohttp import web
from .config import load_api_keys
import subprocess
import sys
import asyncio
import shlex
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
llm_api_keys = load_api_keys(config_path)
llm_api_key=llm_api_keys.get("openai_api_key", "").strip()
llm_base_url=llm_api_keys.get("base_url", "").strip()
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

# 全局变量来跟踪FastAPI和Streamlit服务器的状态
fastapi_process = None
streamlit_process = None

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

def start_server(script_path, port, server_type):
    if server_type == "streamlit":
        cmd = f"{sys.executable} -m streamlit run {script_path} --server.port {port}"
    else:
        cmd = f"{sys.executable} {script_path} --host 127.0.0.1 --port {port}"
    
    logging.info(f"Starting {server_type} server with command: {cmd}")
    
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"  # 确保Python输出不被缓冲
    
    if sys.platform == 'win32':
        return subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
    elif sys.platform == 'darwin':  # macOS
        return subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{cmd}"'], env=env)
    else:  # Linux
        try:
            subprocess.run(['which', 'screen'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            screen_name = f"{server_type}_server"
            full_cmd = f"screen -dmS {screen_name} bash -c '{cmd}'"
            subprocess.run(full_cmd, shell=True, check=True, env=env)
            return subprocess.Popen(['echo', f'{server_type.capitalize()} server started in screen session'])
        except subprocess.CalledProcessError:
            logging.error("Error: 'screen' command not found. Please install screen or use an alternative method.")
            return None

@server.PromptServer.instance.routes.post('/party/fastapi')
async def start_fast_api(request):
    global fastapi_process
    try:
        if fastapi_process is not None and fastapi_process.poll() is None:
            return web.json_response({"status": "success", "message": "FastAPI服务已经在运行"})

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fast_api_path = os.path.join(current_dir, 'fast_api.py')
        
        fastapi_process = start_server(fast_api_path, 8187, "fastapi")
        
        if fastapi_process is None:
            return web.json_response({"status": "error", "message": "无法启动FastAPI服务器"}, status=500)
        
        await asyncio.sleep(5)
        
        if sys.platform != 'win32' and sys.platform != 'darwin':
            return web.json_response({"status": "success", "message": "FastAPI服务已在screen会话中启动"})
        elif fastapi_process.poll() is None:
            return web.json_response({"status": "success", "message": "FastAPI服务已启动"})
        else:
            error_message = "FastAPI启动失败"
            return web.json_response({"status": "error", "message": error_message}, status=500)
    
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

@server.PromptServer.instance.routes.post('/party/streamlit')
async def start_streamlit(request):
    global streamlit_process
    try:
        if streamlit_process is not None and streamlit_process.poll() is None:
            return web.json_response({"status": "success", "message": "Streamlit应用已经在运行"})

        current_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_path = os.path.join(current_dir, 'api.py')
        
        # 尝试多个端口
        for port in range(8501, 8510):
            streamlit_process = start_server(streamlit_path, port, "streamlit")
            if streamlit_process is not None:
                break
        
        if streamlit_process is None:
            logging.error("无法启动Streamlit应用")
            return web.json_response({"status": "error", "message": "无法启动Streamlit应用"}, status=500)
        
        await asyncio.sleep(10)  # 给Streamlit更多时间启动
        
        if sys.platform != 'win32' and sys.platform != 'darwin':
            logging.info("Streamlit应用已在screen会话中启动")
            return web.json_response({"status": "success", "message": "Streamlit应用已在screen会话中启动"})
        elif streamlit_process.poll() is None:
            logging.info("Streamlit应用已启动")
            return web.json_response({"status": "success", "message": "Streamlit应用已启动"})
        else:
            error_message = "Streamlit应用启动失败"
            logging.error(error_message)
            return web.json_response({"status": "error", "message": error_message}, status=500)
    
    except Exception as e:
        logging.exception("启动Streamlit时发生异常")
        return web.json_response({"status": "error", "message": str(e)}, status=500)

# 修改获取工作流列表的函数
def get_workflow_list():
    workflow_dirs = [
        os.path.join(os.path.dirname(__file__), 'workflow'),
        os.path.join(os.path.dirname(__file__), 'workflow_api')
    ]
    workflows = []
    for workflow_dir in workflow_dirs:
        if os.path.exists(workflow_dir):
            workflows.extend([f for f in os.listdir(workflow_dir) if f.endswith('.json')])
        else:
            logging.warning(f"工作流目录不存在: {workflow_dir}")
    return workflows

# 修改加载工作流的函数
def load_workflow(workflow_name):
    workflow_dirs = [
        os.path.join(os.path.dirname(__file__), 'workflow'),
        os.path.join(os.path.dirname(__file__), 'workflow_api')
    ]
    for workflow_dir in workflow_dirs:
        workflow_path = os.path.join(workflow_dir, workflow_name)
        if os.path.exists(workflow_path):
            logging.info(f"尝试加载工作流: {workflow_path}")
            try:
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                logging.info(f"成功加载工作流: {workflow_name}")
                return workflow_data
            except json.JSONDecodeError as e:
                logging.error(f"JSON解析错误: {str(e)}")
                raise
            except Exception as e:
                logging.error(f"加载工作流时发生错误: {str(e)}")
                raise
    logging.error(f"工作流文件不存在: {workflow_name}")
    raise FileNotFoundError(f"工作流文件不存在: {workflow_name}")

# 修改获取工作流列表的路由
@server.PromptServer.instance.routes.get('/party/workflow_list')
async def get_workflows(request):
    try:
        workflows = get_workflow_list()
        return web.json_response(workflows)
    except Exception as e:
        logging.error(f"获取工作流列表时发生错误: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)

# 修改加载选定工作流的路由
@server.PromptServer.instance.routes.post('/party/load_workflow')
async def load_selected_workflow(request):
    try:
        data = await request.json()
        workflow_name = data['workflow']
        logging.info(f"尝试加载工作流: {workflow_name}")
        workflow_data = load_workflow(workflow_name)
        logging.info(f"成功加载工作流数据")
        return web.json_response(workflow_data)
    except FileNotFoundError as e:
        logging.error(f"文件未找到: {str(e)}")
        return web.json_response({"status": "error", "message": str(e)}, status=404)
    except json.JSONDecodeError as e:
        logging.error(f"JSON解析错误: {str(e)}")
        return web.json_response({"status": "error", "message": f"无效的JSON文件: {str(e)}"}, status=400)
    except Exception as e:
        logging.error(f"加载工作流时发生错误: {str(e)}")
        logging.error(traceback.format_exc())
        return web.json_response({"status": "error", "message": str(e)}, status=500)

# ... (保持其他路由和函数不变)
