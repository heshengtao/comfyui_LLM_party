import configparser
import os
import openai
import server
from aiohttp import web
from .config import load_api_keys
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
