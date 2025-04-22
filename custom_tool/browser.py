from langchain_openai import ChatOpenAI,AzureChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from browser_use import Agent
import asyncio
import os
import openai
import json
import locale
the_provider = "openai"
the_model = "gpt-4o"

current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir_path, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)


# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
config_key = configparser.ConfigParser()
config_key.read(config_path, encoding="utf-8")
def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


class browser_use_tool:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "gpt-4o",}),
                "provider": (["openai","azure","anthropic"], {"default": "openai",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/自动化（Automation）"

    def file(
        self,
        model_name,
        provider,
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        global the_provider,the_model
        the_provider = provider
        the_model = model_name
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        if openai.api_key == "":
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        output = [
            {
                "type": "function",
                "function": {
                    "name": "browser_use",
                    "description": "用浏览器自动执行你给出的任务的工具，输入任务描述，返回任务执行结果",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string", "description": "要执行的任务描述"},
                        },
                        "required": ["task"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
    
async def browser(task,llm):
    agent = Agent(
        task=task,
        llm=llm,
    )
    result = await agent.run()
    return result

def browser_use(task):
    global the_provider,the_model 
    if the_provider == "openai":
        llm=ChatOpenAI(model=the_model,base_url=openai.base_url,api_key=openai.api_key)
    elif the_provider == "azure":
        llm=AzureChatOpenAI(model=the_model,base_url=openai.base_url,api_key=openai.api_key)
    elif the_provider == "anthropic":
        llm=ChatAnthropic(model=the_model,anthropic_api_url=openai.base_url,anthropic_api_key=openai.api_key)
    res=asyncio.run(browser(task, llm))
    last_model_output = res.final_result()
    return str(last_model_output)

_TOOL_HOOKS = ["browser_use"]
NODE_CLASS_MAPPINGS = {
    "browser_use_tool": browser_use_tool,
}
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'



try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "browser_use_tool": "☁️浏览器自动控制工具"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "browser_use_tool": "☁️Browser Automatic Control Tool"
    }
