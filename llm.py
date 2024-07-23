import base64
import datetime
import gc
import glob
import hashlib
import importlib
import io
import json
import os
import re
import sys
import time
import traceback

import numpy as np
import openai
import requests
import torch
from PIL import Image
from transformers import (
    AutoModel,
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
)

if torch.cuda.is_available():
    from transformers import BitsAndBytesConfig

from torchvision.transforms import ToPILImage

from .config import config_key, config_path, current_dir_path, load_api_keys
from .tools.api_tool import (
    api_function,
    api_tool,
    list_append,
    list_append_plus,
    list_extend,
    list_extend_plus,
    parameter_combine,
    parameter_combine_plus,
    parameter_function,
    use_api_tool,
)
from .tools.arxiv import arxiv_tool, get_arxiv
from .tools.check_web import check_web, check_web_tool
from .tools.classify_function import classify_function, classify_function_plus
from .tools.classify_persona import classify_persona, classify_persona_plus
from .tools.clear_model import clear_model
from .tools.CosyVoice import CosyVoice
from .tools.custom_persona import custom_persona
from .tools.dialog import end_dialog, start_dialog
from .tools.dingding import Dingding, Dingding_tool, send_dingding
from .tools.end_work import end_workflow
from .tools.excel import image_iterator, load_excel
from .tools.feishu import feishu, feishu_tool, send_feishu
from .tools.file_combine import file_combine, file_combine_plus
from .tools.get_time import get_time, time_tool
from .tools.get_weather import (
    accuweather_tool,
    get_accuweather,
    get_weather,
    weather_tool,
)
from .tools.git_tool import github_tool, search_github_repositories
from .tools.image import CLIPTextEncode_party, KSampler_party, VAEDecode_party
from .tools.interpreter import interpreter, interpreter_tool
from .tools.keyword import keyword_tool, load_keyword, search_keyword
from .tools.KG import (
    Delete_entities,
    Delete_relationships,
    Inquire_entities,
    Inquire_entity_list,
    Inquire_entity_relationships,
    Inquire_relationships,
    KG_json_toolkit_developer,
    KG_json_toolkit_user,
    Modify_entities,
    Modify_relationships,
    New_entities,
    New_relationships,
)
from .tools.KG_csv import (
    Delete_triple,
    Inquire_triple,
    KG_csv_toolkit_developer,
    KG_csv_toolkit_user,
    New_triple,
)
from .tools.KG_neo4j import (
    Delete_entities_neo4j,
    Delete_relationships_neo4j,
    Inquire_entities_neo4j,
    Inquire_entity_list_neo4j,
    Inquire_entity_relationships_neo4j,
    Inquire_relationships_neo4j,
    KG_neo_toolkit_developer,
    KG_neo_toolkit_user,
    Modify_entities_neo4j,
    Modify_relationships_neo4j,
    New_entities_neo4j,
    New_relationships_neo4j,
)
from .tools.load_ebd import data_base, ebd_tool, load_embeddings,save_ebd_database
from .tools.load_file import load_file, load_file_folder, load_url, start_workflow
from .tools.load_model_name import load_name
from .tools.load_persona import load_persona
from .tools.logic import get_string, replace_string, string_logic, substring
from .tools.new_interpreter import new_interpreter, new_interpreter_tool
from .tools.omost import omost_decode, omost_setting
from .tools.search_web import (
    bing_loader,
    bing_tool,
    google_loader,
    google_tool,
    search_web,
    search_web_bing,
)
from .tools.show_text import About_us, show_text_party
from .tools.story import read_story_json, story_json_tool
from .tools.text_iterator import text_iterator
from .tools.tool_combine import tool_combine, tool_combine_plus
from .tools.translate_persona import translate_persona
from .tools.tts import openai_tts, play_audio
from .tools.wechat import send_wechat, work_wechat, work_wechat_tool
from .tools.whisper import listen_audio, openai_whisper
from .tools.wikipedia import get_wikipedia, load_wikipedia, wikipedia_tool
from .tools.workflow import work_flow, workflow_tool, workflow_transfer

_TOOL_HOOKS = [
    "get_time",
    "get_weather",
    "search_web",
    "search_web_bing",
    "check_web",
    "interpreter",
    "data_base",
    "another_llm",
    "new_interpreter",
    "use_api_tool",
    "get_accuweather",
    "get_wikipedia",
    "get_arxiv",
    "work_flow",
    "search_github_repositories",
    "send_wechat",
    "send_dingding",
    "send_feishu",
    "search_keyword",
    "read_story_json",
    "Inquire_entities",
    "New_entities",
    "Modify_entities",
    "Delete_entities",
    "Inquire_relationships",
    "New_relationships",
    "Modify_relationships",
    "Delete_relationships",
    "Inquire_triple",
    "New_triple",
    "Delete_triple",
    "Inquire_entity_relationships",
    "Inquire_entity_list",
    "Inquire_entities_neo4j",
    "New_entities_neo4j",
    "Modify_entities_neo4j",
    "Delete_entities_neo4j",
    "Inquire_relationships_neo4j",
    "New_relationships_neo4j",
    "Modify_relationships_neo4j",
    "Delete_relationships_neo4j",
    "Inquire_entity_relationships_neo4j",
    "Inquire_entity_list_neo4j",
]
instances = []
image_buffer = []


def another_llm(id, type, question):
    print(id, type, question)
    global instances
    if type == "api":
        try:
            llm = next((instance for instance in instances if str(instance.id).strip() == str(id).strip()), None)
        except:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        if llm is None:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        (
            main_brain,
            system_prompt,
            model,
            temperature,
            is_memory,
            is_tools_in_sys_prompt,
            is_locked,
            max_length,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            images,
            imgbb_api_key,
            conversation_rounds,
            historical_record,
        ) = llm.list
        res, _, _, _ = llm.chatbot(
            question,
            main_brain,
            system_prompt,
            model,
            temperature,
            is_memory,
            is_tools_in_sys_prompt,
            is_locked,
            max_length,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            images,
            imgbb_api_key,
            conversation_rounds,
            historical_record,
        )
    elif type == "local":
        try:
            llm = next((instance for instance in instances if str(instance.id).strip() == str(id).strip()), None)
        except:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        if llm is None:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        (
            main_brain,
            system_prompt,
            model_type,
            model,
            tokenizer,
            temperature,
            max_length,
            is_memory,
            is_locked,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            image,
            conversation_rounds,
            historical_record,
        ) = llm.list
        res, _, _, _ = llm.chatbot(
            question,
            main_brain,
            system_prompt,
            model_type,
            model,
            tokenizer,
            temperature,
            max_length,
            is_memory,
            is_locked,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            image,
            conversation_rounds,
            historical_record,
        )
    else:
        return "type参数错误，请使用api或local"
    print(res)
    return "你调用的智能助手的问答是：" + res + "\n请根据以上回答，回答用户的问题。"


llm_tools_list = []
llm_tools = [
    {
        "type": "function",
        "function": {
            "name": "another_llm",
            "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："
            + json.dumps(llm_tools_list, ensure_ascii=False, indent=4),
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "智能助手的id"},
                    "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                    "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
                },
                "required": ["id", "type", "question"],
            },
        },
    }
]


def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if "multi_tool_use." in tool_name:
        tool_name = tool_name.replace("multi_tool_use.", "")
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = globals().get(tool_name)
    try:
        ret_out = tool_call(**tool_params)
        if tool_name == "work_flow":
            ret = ret_out[0]
            image_buffer = ret_out[1]
            if ret == "" or ret is None:
                ret = "图片已生成。"
        else:
            ret = ret_out
    except:
        ret = traceback.format_exc()
    return str(ret)


class Chat:
    def __init__(self, model_name, apikey, baseurl) -> None:
        self.model_name = model_name
        self.apikey = apikey
        self.baseurl = baseurl

    def send(self, user_prompt, temperature, max_length, history, tools=None):
        try:
            openai.api_key = self.apikey
            openai.base_url = self.baseurl
            new_message = {"role": "user", "content": user_prompt}
            history.append(new_message)
            print(history)
            if tools is not None:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=history,
                    temperature=temperature,
                    tools=tools,
                    max_tokens=max_length,
                )
                while response.choices[0].message.tool_calls:
                    assistant_message = response.choices[0].message
                    response_content = assistant_message.tool_calls[0].function
                    print("正在调用" + response_content.name + "工具")
                    print(response_content.arguments)
                    results = dispatch_tool(response_content.name, json.loads(response_content.arguments))
                    print(results)
                    history.append(
                        {
                            "tool_calls": [
                                {
                                    "id": assistant_message.tool_calls[0].id,
                                    "function": {
                                        "arguments": response_content.arguments,
                                        "name": response_content.name,
                                    },
                                    "type": assistant_message.tool_calls[0].type,
                                }
                            ],
                            "role": "assistant",
                            "content": str(response_content),
                        }
                    )
                    history.append(
                        {
                            "role": "tool",
                            "tool_call_id": assistant_message.tool_calls[0].id,
                            "name": response_content.name,
                            "content": results,
                        }
                    )
                    try:
                        response = openai.chat.completions.create(
                            model=self.model_name,
                            messages=history,
                            tools=tools,
                            temperature=temperature,
                            max_tokens=max_length,
                        )
                        print(response)
                    except Exception as e:
                        print("tools calling失败，尝试使用function calling" + str(e))
                        # 删除history最后两个元素
                        history.pop()
                        history.pop()
                        history.append(
                            {
                                "role": "assistant",
                                "content": str(response_content),
                                "function_call": {
                                    "name": response_content.name,
                                    "arguments": response_content.arguments,
                                },
                            }
                        )
                        history.append({"role": "function", "name": response_content.name, "content": results})
                        response = openai.chat.completions.create(
                            model=self.model_name,
                            messages=history,
                            tools=tools,
                            temperature=temperature,
                            max_tokens=max_length,
                        )
                        print(response)
                while response.choices[0].message.function_call:
                    assistant_message = response.choices[0].message
                    function_call = assistant_message.function_call
                    function_name = function_call.name
                    function_arguments = json.loads(function_call.arguments)
                    print("正在调用" + function_name + "工具")
                    results = dispatch_tool(function_name, function_arguments)
                    print(results)
                    history.append(
                        {
                            "role": "assistant",
                            "content": str(function_call),
                            "function_call": {"name": function_name, "arguments": function_arguments},
                        }
                    )
                    history.append({"role": "function", "name": function_name, "content": results})
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=history,
                        tools=tools,
                        temperature=temperature,
                        max_tokens=max_length,
                    )
                response_content = response.choices[0].message.content
                print(response)
                # 正则表达式匹配
                pattern = r'\{\s*"tool":\s*"(.*?)",\s*"parameters":\s*\{(.*?)\}\s*\}'
                while re.search(pattern, response_content, re.DOTALL) != None:
                    match = re.search(pattern, response_content, re.DOTALL)
                    tool = match.group(1)
                    parameters = match.group(2)
                    json_str = '{"tool": "' + tool + '", "parameters": {' + parameters + "}}"
                    print("正在调用" + tool + "工具")
                    parameters = json.loads("{" + parameters + "}")
                    results = dispatch_tool(tool, parameters)
                    print(results)
                    history.append({"role": "assistant", "content": json_str})
                    history.append(
                        {
                            "role": "user",
                            "content": "调用"
                            + tool
                            + "工具返回的结果为："
                            + results
                            + "。请根据工具返回的结果继续回答我之前提出的问题。",
                        }
                    )
                    response = openai.chat.completions.create(
                        model=self.model_name, messages=history, temperature=temperature, max_tokens=max_length
                    )
                    response_content = response.choices[0].message.content
            else:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=history,
                    temperature=temperature,
                    max_tokens=max_length,
                )
            response_content = response.choices[0].message.content
            history.append({"role": "assistant", "content": response_content})
        except Exception as ex:
            response_content = str(ex)
        return response_content, history


class LLM_api_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "gpt-3.5-turbo-1106"}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def chatbot(self, model_name, base_url=None, api_key=None):
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            openai.base_url = base_url
        elif model_name in config_key:
            api_keys = config_key[model_name]
            openai.base_url = api_keys.get("base_url")
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")
        if openai.api_key == "":
            return ("请输入API_KEY",)
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        chat = Chat(model_name, openai.api_key, openai.base_url)
        return (chat,)


class LLM:
    original_IS_CHANGED = None

    def __init__(self):
        current_time = datetime.datetime.now()
        # 以时间戳作为ID，字符串格式 XX年XX月XX日XX时XX分XX秒
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        global instances
        instances.append(self)
        # 构建prompt.json的绝对路径，如果temp文件夹不存在就创建
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(current_dir_path, "temp"), exist_ok=True)
        self.prompt_path = os.path.join(current_dir_path, "temp", str(self.id) + ".json")
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(
                    [{"role": "system", "content": "你是一个强大的人工智能助手。"}], f, indent=4, ensure_ascii=False
                )
        self.tool_data = {"id": self.id, "system_prompt": "", "type": "api"}
        self.list = []
        self.added_to_list = False
        self.is_locked = "disable"

    @classmethod
    def INPUT_TYPES(s):
        temp_path = os.path.join(current_dir_path, "temp")
        full_paths = [os.path.join(temp_path, f) for f in os.listdir(temp_path)]
        full_paths.sort(key=os.path.getmtime, reverse=True)
        paths = [os.path.basename(f) for f in full_paths]
        paths.insert(0, "")
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": "你一个强大的人工智能助手。"}),
                "user_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "你好",
                    },
                ),
                "model": ("CUSTOM", {}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "is_memory": (["enable", "disable"], {"default": "enable"}),
                "is_tools_in_sys_prompt": (["enable", "disable"], {"default": "disable"}),
                "is_locked": (["enable", "disable"], {"default": "disable"}),
                "main_brain": (["enable", "disable"], {"default": "enable"}),
                "max_length": ("FLOAT", {"default": 1920, "min": 256, "max": 128000, "step": 128}),
            },
            "optional": {
                "system_prompt_input": ("STRING", {"forceInput": True}),
                "user_prompt_input": ("STRING", {"forceInput": True}),
                "tools": ("STRING", {"forceInput": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "images": ("IMAGE", {"forceInput": True}),
                "imgbb_api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
                "conversation_rounds": ("INT", {"default": 100, "min": 1, "max": 10000}),
                "historical_record": (paths, {"default": ""}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "IMAGE",
    )
    RETURN_NAMES = (
        "assistant_response",
        "history",
        "tool",
        "image",
    )

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型链（model_chain）"

    def chatbot(
        self,
        user_prompt,
        main_brain,
        system_prompt,
        model,
        temperature,
        is_memory,
        is_tools_in_sys_prompt,
        is_locked,
        max_length,
        system_prompt_input="",
        user_prompt_input="",
        tools=None,
        file_content=None,
        images=None,
        imgbb_api_key=None,
        conversation_rounds=100,
        historical_record="",
    ):
        self.list = [
            main_brain,
            system_prompt,
            model,
            temperature,
            is_memory,
            is_tools_in_sys_prompt,
            is_locked,
            max_length,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            images,
            imgbb_api_key,
            conversation_rounds,
            historical_record,
        ]
        if user_prompt is None:
            user_prompt = user_prompt_input
        else:
            user_prompt = user_prompt + user_prompt_input
        if historical_record != "":
            temp_path = os.path.join(current_dir_path, "temp")
            self.prompt_path = os.path.join(temp_path, historical_record)
        self.tool_data["system_prompt"] = system_prompt
        if system_prompt_input is not None and system_prompt is not None:
            system_prompt = system_prompt + system_prompt_input
        elif system_prompt is None:
            system_prompt = system_prompt_input
        global llm_tools_list, llm_tools
        if main_brain == "disable":
            if self.added_to_list == False:
                llm_tools_list.append(self.tool_data)
                self.added_to_list = True
        self.is_locked = is_locked
        if LLM.original_IS_CHANGED is None:
            # 保存原始的IS_CHANGED方法的引用
            LLM.original_IS_CHANGED = LLM.IS_CHANGED
        if self.is_locked == "disable":
            setattr(LLM, "IS_CHANGED", LLM.original_IS_CHANGED)
        else:
            # 如果方法存在，则删除
            if hasattr(LLM, "IS_CHANGED"):
                delattr(LLM, "IS_CHANGED")
        llm_tools = [
            {
                "type": "function",
                "function": {
                    "name": "another_llm",
                    "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："
                    + json.dumps(llm_tools_list, ensure_ascii=False, indent=4),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "智能助手的id"},
                            "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                            "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
                        },
                        "required": ["id", "type", "question"],
                    },
                },
            }
        ]

        llm_tools_json = json.dumps(llm_tools, ensure_ascii=False, indent=4)
        if user_prompt is None or user_prompt.strip() == "":
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            return (
                "",
                str(history),
                llm_tools_json,
                None,
            )
        else:
            try:
                if is_memory == "disable":
                    with open(self.prompt_path, "w", encoding="utf-8") as f:
                        json.dump([{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False)
                api_keys = load_api_keys(config_path)

                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                history_temp = [history[0]]
                elements_to_keep = 2 * conversation_rounds
                if elements_to_keep < len(history) - 1:
                    history_temp += history[-elements_to_keep:]
                    history_copy = history[1:-elements_to_keep]
                else:
                    if len(history) > 1:
                        history_temp += history[1:]
                    history_copy = []
                if len(history_temp) > 1:
                    if history_temp[1]["role"] == "tool":
                        history_temp.insert(1, history[-elements_to_keep - 1])
                        if -elements_to_keep - 1 > 1:
                            history_copy = history[1 : -elements_to_keep - 1]
                        else:
                            history_copy = []
                history = history_temp
                for message in history:
                    if message["role"] == "system":
                        message["content"] = system_prompt
                if is_tools_in_sys_prompt == "enable":
                    tools_list = []
                    GPT_INSTRUCTION = ""
                    if tools is not None:
                        tools_dis = json.loads(tools)
                        for tool_dis in tools_dis:
                            tools_list.append(tool_dis["function"])
                        tools_instructions = ""
                        tools_instruction_list = []
                        for tool in tools_list:
                            tools_instruction_list.append(tool["name"])
                            tools_instructions += (
                                str(tool["name"])
                                + ":"
                                + "Call this tool to interact with the "
                                + str(tool["name"])
                                + " API. What is the "
                                + str(tool["name"])
                                + " API useful for? "
                                + str(tool["description"])
                                + ". Parameters:"
                                + str(tool["parameters"])
                                + "Required parameters:"
                                + str(tool["parameters"]["required"])
                                + "\n"
                            )
                        REUTRN_FORMAT = '{"tool": "tool name", "parameters": {"parameter name": "parameter value"}}'
                        TOOL_EAXMPLE = 'You will receive a JSON string containing a list of callable tools. Please parse this JSON string and return a JSON object containing the tool name and tool parameters. Here is an example of the tool list:\n\n{"tools": [{"name": "plus_one", "description": "Add one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}},{"name": "minus_one", "description": "Minus one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}}]}\n\nBased on this tool list, generate a JSON object to call a tool. For example, if you need to add one to number 77, return:\n\n{"tool": "plus_one", "parameters": {"number": "77"}}\n\nPlease note that the above is just an example and does not mean that the plus_one and minus_one tools are currently available.'
                        GPT_INSTRUCTION = f"""
        Answer the following questions as best you can. You have access to the following APIs:
        {tools_instructions}

        Use the following format:
        ```tool_json
        {REUTRN_FORMAT}
        ```

        Please choose the appropriate tool according to the user's question. If you don't need to call it, please reply directly to the user's question. When the user communicates with you in a language other than English, you need to communicate with the user in the same language.

        When you have enough information from the tool results, respond directly to the user with a text message without having to call the tool again.
        """

                    for message in history:
                        if message["role"] == "system":
                            message["content"] = system_prompt
                            if tools_list != []:
                                message["content"] += "\n" + TOOL_EAXMPLE + "\n" + GPT_INSTRUCTION + "\n"

                if tools is not None:
                    print(tools)
                    tools = json.loads(tools)

                max_length = int(max_length)

                if file_content is not None:
                    user_prompt = (
                        "文件中相关内容："
                        + file_content
                        + "\n"
                        + "用户提问："
                        + user_prompt
                        + "\n"
                        + "请根据文件内容回答用户问题。\n"
                        + "如果无法从文件内容中找到答案，请回答“抱歉，我无法从文件内容中找到答案。”"
                    )

                if images is not None:
                    if imgbb_api_key == "" or imgbb_api_key is None:
                        imgbb_api_key = api_keys.get("imgbb_api")
                    if imgbb_api_key == "" or imgbb_api_key is None:
                        i = 255.0 * images[0].cpu().numpy()
                        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                        # 将图片保存到缓冲区
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        # 将图片编码为base64
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        img_json = [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img_str}"},
                            },
                        ]
                        user_prompt = img_json
                    else:
                        i = 255.0 * images[0].cpu().numpy()
                        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                        # 将图片保存到缓冲区
                        buffered = io.BytesIO()
                        img.save(buffered, format="PNG")
                        # 将图片编码为base64
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        url = "https://api.imgbb.com/1/upload"
                        payload = {"key": imgbb_api_key, "image": img_str}
                        # 向API发送POST请求
                        response = requests.post(url, data=payload)
                        # 检查请求是否成功
                        if response.status_code == 200:
                            # 解析响应以获取图片URL
                            result = response.json()
                            img_url = result["data"]["url"]
                        else:
                            return "Error: " + response.text
                        img_json = [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_url,
                                },
                            },
                        ]
                        user_prompt = img_json

                response, history = model.send(user_prompt, temperature, max_length, history, tools)
                print(response)
                # 修改prompt.json文件
                history_get = [history[0]]
                history_get.extend(history_copy)
                history_get.extend(history[1:])
                history = history_get
                with open(self.prompt_path, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                for his in history:
                    if his["role"] == "user":
                        # 如果his["content"]是个列表，则只保留"type" : "text"时的"text"属性内容
                        if isinstance(his["content"], list):
                            for item in his["content"]:
                                if item.get("type") == "text" and item.get("text"):
                                    his["content"] = item["text"]
                                    break
                historys = ""
                # 将history中的消息转换成便于用户阅读的markdown格式
                for his in history:
                    if his["role"] == "user":
                        historys += f"**User:** {his['content']}\n\n"
                    elif his["role"] == "assistant":
                        historys += f"**Assistant:** {his['content']}\n\n"
                    elif his["role"] == "system":
                        historys += f"**System:** {his['content']}\n\n"
                    elif his["role"] == "observation":
                        historys += f"**Observation:** {his['content']}\n\n"
                    elif his["role"] == "tool":
                        historys += f"**Tool:** {his['content']}\n\n"
                    elif his["role"] == "function":
                        historys += f"**Function:** {his['content']}\n\n"

                history = str(historys)
                global image_buffer
                image_out = image_buffer.copy()
                image_buffer = []
                if image_out == []:
                    image_out = None
                return (
                    response,
                    history,
                    llm_tools_json,
                    image_out,
                )
            except Exception as ex:
                print(ex)
                return (
                    str(ex),
                    str(ex),
                    llm_tools_json,
                    None,
                )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


def llm_chat(model, tokenizer, user_prompt, history, device, max_length, role="user", temperature=0.7):
    history.append({"role": role, "content": user_prompt.strip()})
    text = tokenizer.apply_chat_template(history, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(
        model_inputs.input_ids, max_new_tokens=max_length, temperature=temperature  # Add the eos_token_id parameter
    )
    generated_ids = [
        output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    history.append({"role": "assistant", "content": response})
    return response, history


class LLM_local_loader:
    original_IS_CHANGED = None

    def __init__(self):
        self.id = hash(str(self))
        self.device = ""
        self.dtype = ""
        self.model_type = ""
        self.model_path = ""
        self.tokenizer_path = ""
        self.model = ""
        self.tokenizer = ""
        self.is_locked = False

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": ""}),
                "model_type": (
                    ["GLM", "llama", "Qwen"],
                    {
                        "default": "GLM",
                    },
                ),
                "model_path": (
                    "STRING",
                    {
                        "default": None,
                    },
                ),
                "tokenizer_path": (
                    "STRING",
                    {
                        "default": None,
                    },
                ),
                "device": (
                    ["auto", "cuda", "cpu", "mps"],
                    {
                        "default": "auto",
                    },
                ),
                "dtype": (
                    ["float32", "float16", "int8", "int4"],
                    {
                        "default": "float32",
                    },
                ),
                "is_locked": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (
        "CUSTOM",
        "CUSTOM",
    )
    RETURN_NAMES = (
        "model",
        "tokenizer",
    )

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def chatbot(self, model_name, model_type, model_path, tokenizer_path, device, dtype, is_locked=False):
        self.is_locked = is_locked
        if LLM_local_loader.original_IS_CHANGED is None:
            # 保存原始的IS_CHANGED方法的引用
            LLM_local_loader.original_IS_CHANGED = LLM_local_loader.IS_CHANGED
        if self.is_locked == False:
            setattr(LLM_local_loader, "IS_CHANGED", LLM_local_loader.original_IS_CHANGED)
        else:
            # 如果方法存在，则删除
            if hasattr(LLM_local_loader, "IS_CHANGED"):
                delattr(LLM_local_loader, "IS_CHANGED")
        if model_path != "" and tokenizer_path != "":
            model_name = ""
        if model_name in config_key:
            model_path = config_key[model_name].get("model_path")
            tokenizer_path = config_key[model_name].get("tokenizer_path")
        elif model_name != "":
            model_path = model_name
            tokenizer_path = model_name
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        if (
            self.model_type != model_type
            or self.device != device
            or self.dtype != dtype
            or self.model_path != model_path
            or self.tokenizer_path != tokenizer_path
            or is_locked == False
        ):
            del self.model
            del self.tokenizer
            if self.device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()
            # 对于 CPU 和 MPS 设备，不需要清空 CUDA 缓存
            elif self.device == "cpu" or self.device == "mps":
                gc.collect()
            self.model = ""
            self.tokenizer = ""
            self.model_type = model_type
            self.model_path = model_path
            self.tokenizer_path = tokenizer_path
            self.device = device
            self.dtype = dtype
        if model_type == "GLM":
            if self.tokenizer == "":
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
            if self.model == "":
                if device == "cuda":
                    if dtype == "float32":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()
                    elif dtype == "float16":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
                    elif dtype == "int8":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(8).half().cuda()
                        )
                    elif dtype == "int4":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).half().cuda()
                        )
                elif device == "cpu":
                    if dtype == "float32":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float()
                    elif dtype == "float16":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().float()
                    elif dtype == "int8":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(8).half().float()
                        )
                    elif dtype == "int4":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).half().float()
                        )
                elif device == "mps":
                    if dtype == "float32":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to("mps")
                    elif dtype == "float16":
                        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().to("mps")
                    elif dtype == "int8":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(8).half().to("mps")
                        )
                    elif dtype == "int4":
                        self.model = (
                            AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).half().to("mps")
                        )
                self.model = self.model.eval()

        elif model_type in ["llama", "Qwen"]:
            if self.tokenizer == "":
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
            if self.model == "":
                if device == "cuda":
                    if dtype == "float32":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cuda"
                        )
                    elif dtype == "float16":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cuda"
                        ).half()
                    elif dtype == "int8":
                        quantization_config = BitsAndBytesConfig(
                            load_in_8bit=True,
                        )
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path,
                            trust_remote_code=True,
                            device_map="cuda",
                            quantization_config=quantization_config,
                        )
                    elif dtype == "int4":
                        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path,
                            trust_remote_code=True,
                            device_map="cuda",
                            quantization_config=quantization_config,
                        )
                elif device == "cpu":
                    if dtype == "float32":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cpu"
                        )
                    elif dtype == "float16":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cpu"
                        ).half()
                    elif dtype == "int8":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cpu"
                        ).half()
                    elif dtype == "int4":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="cpu"
                        ).half()
                elif device == "mps":
                    if dtype == "float32":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="mps"
                        )
                    elif dtype == "float16":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="mps"
                        ).half()
                    elif dtype == "int8":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="mps"
                        ).half()
                    elif dtype == "int4":
                        self.model = AutoModelForCausalLM.from_pretrained(
                            model_path, trust_remote_code=True, device_map="mps"
                        ).half()
                self.model = self.model.eval()
        return (
            self.model,
            self.tokenizer,
        )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


class LLM_local:
    original_IS_CHANGED = None

    def __init__(self):
        # 生成一个hash值作为id
        current_time = datetime.datetime.now()
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        global instances
        instances.append(self)
        # 构建prompt.json的绝对路径，如果temp文件夹不存在就创建
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(current_dir_path, "temp"), exist_ok=True)
        self.prompt_path = os.path.join(current_dir_path, "temp", str(self.id) + ".json")
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, "w", encoding="utf-8") as f:
                json.dump(
                    [{"role": "system", "content": "你是一个强大的人工智能助手。"}], f, indent=4, ensure_ascii=False
                )
        self.tool_data = {"id": self.id, "system_prompt": "", "type": "local"}
        self.list = []
        self.added_to_list = False
        self.is_locked = "disable"

    @classmethod
    def INPUT_TYPES(s):
        temp_path = os.path.join(current_dir_path, "temp")
        full_paths = [os.path.join(temp_path, f) for f in os.listdir(temp_path)]
        full_paths.sort(key=os.path.getmtime, reverse=True)
        paths = [os.path.basename(f) for f in full_paths]
        paths.insert(0, "")
        return {
            "required": {
                "model": ("CUSTOM", {}),
                "system_prompt": ("STRING", {"multiline": True, "default": "你一个强大的人工智能助手。"}),
                "user_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "你好",
                    },
                ),
                "model_type": (
                    ["GLM", "llama", "Qwen", "llaVa", "llama-guff"],
                    {
                        "default": "GLM",
                    },
                ),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_length": ("FLOAT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
                "is_memory": (["enable", "disable"], {"default": "enable"}),
                "is_locked": (["enable", "disable"], {"default": "disable"}),
                "main_brain": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "tokenizer": ("CUSTOM", {}),
                "image": ("IMAGE", {"forceInput": True}),
                "system_prompt_input": ("STRING", {"forceInput": True}),
                "user_prompt_input": ("STRING", {"forceInput": True}),
                "tools": ("STRING", {"forceInput": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "conversation_rounds": ("INT", {"default": 100, "min": 1, "max": 10000}),
                "historical_record": (paths, {"default": ""}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "IMAGE",
    )
    RETURN_NAMES = (
        "assistant_response",
        "history",
        "tool",
        "image",
    )

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型链（model_chain）"

    def chatbot(
        self,
        user_prompt,
        main_brain,
        system_prompt,
        model_type,
        model,
        tokenizer=None,
        temperature=0.7,
        max_length=2048,
        is_memory="enable",
        is_locked="disable",
        system_prompt_input="",
        user_prompt_input="",
        tools=None,
        file_content=None,
        image=None,
        conversation_rounds=100,
        historical_record=None,
    ):
        self.list = [
            main_brain,
            system_prompt,
            model_type,
            model,
            tokenizer,
            temperature,
            max_length,
            is_memory,
            is_locked,
            system_prompt_input,
            user_prompt_input,
            tools,
            file_content,
            image,
            conversation_rounds,
            historical_record,
        ]
        if user_prompt is None:
            user_prompt = user_prompt_input
        else:
            user_prompt = user_prompt + user_prompt_input
        if historical_record != "":
            temp_path = os.path.join(current_dir_path, "temp")
            self.prompt_path = os.path.join(temp_path, historical_record)
        self.tool_data["system_prompt"] = system_prompt
        if system_prompt_input is not None and system_prompt is not None:
            system_prompt = system_prompt + system_prompt_input
        elif system_prompt is None:
            system_prompt = system_prompt_input
        global llm_tools_list, llm_tools
        if main_brain == "disable":
            if not self.added_to_list:
                llm_tools_list.append(self.tool_data)
                self.added_to_list = True
        self.is_locked = is_locked
        if LLM_local.original_IS_CHANGED is None:
            # 保存原始的IS_CHANGED方法的引用
            LLM_local.original_IS_CHANGED = LLM_local.IS_CHANGED
        if self.is_locked == "disable":
            setattr(LLM_local, "IS_CHANGED", LLM_local.original_IS_CHANGED)
        else:
            # 如果方法存在，则删除
            if hasattr(LLM_local, "IS_CHANGED"):
                delattr(LLM_local, "IS_CHANGED")
        llm_tools = [
            {
                "type": "function",
                "function": {
                    "name": "another_llm",
                    "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："
                    + json.dumps(llm_tools_list, ensure_ascii=False, indent=4),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "智能助手的id"},
                            "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                            "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
                        },
                        "required": ["id", "type", "question"],
                    },
                },
            }
        ]
        llm_tools_json = json.dumps(llm_tools, ensure_ascii=False, indent=4)
        if user_prompt is None or user_prompt.strip() == "":
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            return (
                "",
                str(history),
                llm_tools_json,
            )
        else:
            try:
                if is_memory == "disable":
                    with open(self.prompt_path, "w", encoding="utf-8") as f:
                        json.dump([{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False)
                with open(self.prompt_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                history_temp = [history[0]]
                elements_to_keep = 2 * conversation_rounds
                if elements_to_keep < len(history) - 1:
                    history_temp += history[-elements_to_keep:]
                    history_copy = history[1:-elements_to_keep]
                else:
                    if len(history) > 1:
                        history_temp += history[1:]
                    history_copy = []
                if len(history_temp) > 1:
                    if history_temp[1]["role"] == "tool":
                        history_temp.insert(1, history[-elements_to_keep - 1])
                        if -elements_to_keep - 1 > 1:
                            history_copy = history[1 : -elements_to_keep - 1]
                        else:
                            history_copy = []
                history = history_temp
                tools_list = []
                GPT_INSTRUCTION = ""
                if tools is not None:
                    tools_dis = json.loads(tools)
                    for tool_dis in tools_dis:
                        tools_list.append(tool_dis["function"])
                    tools_instructions = ""
                    tools_instruction_list = []
                    for tool in tools_list:
                        tools_instruction_list.append(tool["name"])
                        tools_instructions += (
                            str(tool["name"])
                            + ":"
                            + "Call this tool to interact with the "
                            + str(tool["name"])
                            + " API. What is the "
                            + str(tool["name"])
                            + " API useful for? "
                            + str(tool["description"])
                            + ". Parameters:"
                            + str(tool["parameters"])
                            + "Required parameters:"
                            + str(tool["parameters"]["required"])
                            + "\n"
                        )
                    REUTRN_FORMAT = '{"tool": "tool name", "parameters": {"parameter name": "parameter value"}}'
                    TOOL_EAXMPLE = 'You will receive a JSON string containing a list of callable tools. Please parse this JSON string and return a JSON object containing the tool name and tool parameters. Here is an example of the tool list:\n\n{"tools": [{"name": "plus_one", "description": "Add one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}},{"name": "minus_one", "description": "Minus one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}}]}\n\nBased on this tool list, generate a JSON object to call a tool. For example, if you need to add one to number 77, return:\n\n{"tool": "plus_one", "parameters": {"number": "77"}}\n\nPlease note that the above is just an example and does not mean that the plus_one and minus_one tools are currently available.'
                    GPT_INSTRUCTION = f"""
    Answer the following questions as best you can. You have access to the following APIs:
    {tools_instructions}

    Use the following format:
    ```tool_json
    {REUTRN_FORMAT}
    ```

    Please choose the appropriate tool according to the user's question. If you don't need to call it, please reply directly to the user's question. When the user communicates with you in a language other than English, you need to communicate with the user in the same language.

    When you have enough information from the tool results, respond directly to the user with a text message without having to call the tool again.
    """

                for message in history:
                    if message["role"] == "system":
                        message["content"] = system_prompt
                        if tools_list != []:
                            if model_type == "GLM":
                                message["content"] += "\n" + "你可以使用以下工具："
                                message["tools"] = tools_list
                            elif model_type in ["llama", "Qwen", "llaVa", "llama-guff"]:
                                message["content"] += "\n" + TOOL_EAXMPLE + "\n" + GPT_INSTRUCTION + "\n"
                                if "tools" in message:
                                    # 如果存在，移除 'tools' 键值对
                                    message.pop("tools")
                        else:
                            if "tools" in message:
                                # 如果存在，移除 'tools' 键值对
                                message.pop("tools")
                if tools is not None:
                    print(tools)
                    tools = json.loads(tools)

                def is_valid_json(json_str):
                    try:
                        json.loads(json_str)
                        return True
                    except json.JSONDecodeError:
                        return False

                max_length = int(max_length)
                if file_content is not None:
                    user_prompt = (
                        "文件中相关内容："
                        + file_content
                        + "\n"
                        + "用户提问："
                        + user_prompt
                        + "\n"
                        + "请根据文件内容回答用户问题。\n"
                        + "如果无法从文件内容中找到答案，请回答“抱歉，我无法从文件内容中找到答案。”"
                    )

                # 获得model存放的设备
                if model_type not in ["llaVa", "llama-guff"]:
                    device = next(model.parameters()).device
                if model_type == "GLM":
                    response, history = model.chat(
                        tokenizer, user_prompt, history, temperature=temperature, max_length=max_length, role="user"
                    )
                    while type(response) == dict:
                        if response["name"] == "interpreter":
                            result = interpreter(str(response["content"]))
                            response, history = model.chat(tokenizer, result, history=history, role="observation")
                        else:
                            result = dispatch_tool(response["name"], response["parameters"])
                            print(result)
                            response, history = model.chat(tokenizer, result, history=history, role="observation")
                elif model_type in ["llama", "Qwen"]:
                    response, history = llm_chat(
                        model, tokenizer, user_prompt, history, device, max_length, temperature=temperature
                    )
                    # 正则表达式匹配
                    pattern = r'\{\s*"tool":\s*"(.*?)",\s*"parameters":\s*\{(.*?)\}\s*\}'
                    while re.search(pattern, response, re.DOTALL) != None:
                        match = re.search(pattern, response, re.DOTALL)
                        tool = match.group(1)
                        parameters = match.group(2)
                        json_str = '{"tool": "' + tool + '", "parameters": {' + parameters + "}}"
                        history.append({"role": "assistant", "content": json_str})
                        print("正在调用" + tool + "工具")
                        parameters = json.loads("{" + parameters + "}")
                        results = dispatch_tool(tool, parameters)
                        print(results)
                        response, history = llm_chat(
                            model,
                            tokenizer,
                            results,
                            history,
                            device,
                            max_length,
                            role="observation",
                            temperature=temperature,
                        )
                elif model_type == "llama-guff":
                    from llama_cpp import Llama

                    history.append({"role": "user", "content": user_prompt.strip()})
                    response = model.create_chat_completion(
                        messages=history,
                        max_tokens=max_length,
                        temperature=temperature,
                    )
                    response_content = response["choices"][0]["message"]["content"]
                    print(response_content)
                    # 正则表达式匹配
                    pattern = r'\{\s*"tool":\s*"(.*?)",\s*"parameters":\s*\{(.*?)\}\s*\}'
                    while re.search(pattern, response_content, re.DOTALL) != None:
                        match = re.search(pattern, response_content, re.DOTALL)
                        tool = match.group(1)
                        parameters = match.group(2)
                        json_str = '{"tool": "' + tool + '", "parameters": {' + parameters + "}}"
                        print("正在调用" + tool + "工具")
                        results = dispatch_tool(tool, parameters)
                        print(results)
                        history.append({"role": "assistant", "content": json_str})
                        history.append({"role": "observation", "content": results})
                        response = model.create_chat_completion(
                            messages=history,
                            max_tokens=max_length,
                            temperature=temperature,
                        )
                        response_content = response.choices[0].message.content
                elif model_type == "llaVa":
                    if image is not None:
                        pil_image = ToPILImage()(image[0].permute(2, 0, 1))
                        # Convert the PIL image to a bytes buffer
                        buffer = io.BytesIO()
                        pil_image.save(buffer, format="PNG")  # You can change the format if needed
                        # Get the bytes from the buffer
                        image_bytes = buffer.getvalue()
                        # Encode the bytes to base64
                        base64_string = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                        user_content = {
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": base64_string}},
                                {"type": "text", "text": user_prompt},
                            ],
                        }
                        history.append(user_content)
                        response = model.create_chat_completion(
                            messages=history,
                            temperature=temperature,
                            max_tokens=max_length,
                            frequency_penalty=1,
                            presence_penalty=0,
                            repeat_penalty=1.1,
                            stop=["<|eot_id|>", "[/INST]", "</s>", "[End Conversation]"],
                        )
                        response = f"{response['choices'][0]['message']['content']}"
                        print(response)
                        assistant_content = {"role": "assistant", "content": response}
                        history.append(assistant_content)
                    else:
                        user_content = {"role": "user", "content": user_prompt}
                        history.append(user_content)
                        response = model.create_chat_completion(
                            messages=history,
                            temperature=temperature,
                            max_tokens=max_length,
                            frequency_penalty=1,
                            presence_penalty=1,
                            repeat_penalty=1.1,
                            stop=["<|eot_id|>", "[/INST]", "</s>", "[End Conversation]"],
                        )
                        response = f"{response['choices'][0]['message']['content']}"
                        assistant_content = {"role": "assistant", "content": response}
                        history.append(assistant_content)
                print(response)
                # 修改prompt.json文件
                history_get = [history[0]]
                history_get.extend(history_copy)
                history_get.extend(history[1:])
                history = history_get
                with open(self.prompt_path, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                for his in history:
                    if his["role"] == "user":
                        # 如果his["content"]是个列表，则只保留"type" : "text"时的"text"属性内容
                        if isinstance(his["content"], list):
                            for item in his["content"]:
                                if item.get("type") == "text" and item.get("text"):
                                    his["content"] = item["text"]
                                    break
                historys = ""
                # 将history中的消息转换成便于用户阅读的markdown格式
                for his in history:
                    if his["role"] == "user":
                        historys += f"**User:** {his['content']}\n\n"
                    elif his["role"] == "assistant":
                        historys += f"**Assistant:** {his['content']}\n\n"
                    elif his["role"] == "system":
                        historys += f"**System:** {his['content']}\n\n"
                    elif his["role"] == "observation":
                        historys += f"**Observation:** {his['content']}\n\n"
                    elif his["role"] == "tool":
                        historys += f"**Tool:** {his['content']}\n\n"
                    elif his["role"] == "function":
                        historys += f"**Function:** {his['content']}\n\n"

                history = str(historys)
                global image_buffer
                image_out = image_buffer.copy()
                image_buffer = []
                if image_out == []:
                    image_out = None
                return (
                    response,
                    history,
                    llm_tools_json,
                    image_out,
                )
            except Exception as ex:
                print(ex)
                return (
                    str(ex),
                    str(ex),
                    llm_tools_json,
                    None,
                )

    @classmethod
    def IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


class LLavaLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": ""}),
                "ckpt_path": ("STRING", {"default": ""}),
                "clip_path": ("STRING", {"default": ""}),
                "max_ctx": ("INT", {"default": 2048, "min": 300, "max": 100000, "step": 64}),
                "gpu_layers": ("INT", {"default": 27, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llava_checkpoint"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_llava_checkpoint(self, model_name, ckpt_path, max_ctx, gpu_layers, n_threads, clip_path):
        from llama_cpp import Llama
        from llama_cpp.llama_chat_format import Llava15ChatHandler

        if ckpt_path != "" and clip_path != "":
            model_name = ""
        if model_name in config_key:
            ckpt_path = config_key[model_name].get("ckpt_path")
            clip_path = config_key[model_name].get("clip_path")
        clip = Llava15ChatHandler(clip_model_path=clip_path, verbose=False)
        llm = Llama(
            model_path=ckpt_path,
            chat_handler=clip,
            offload_kqv=True,
            f16_kv=True,
            use_mlock=False,
            embedding=False,
            n_batch=1024,
            last_n_tokens_size=1024,
            verbose=True,
            seed=42,
            n_ctx=max_ctx,
            n_gpu_layers=gpu_layers,
            n_threads=n_threads,
            logits_all=True,
            echo=False,
        )
        return (llm,)


class llama_guff_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": ""}),
                "model_path": ("STRING", {"default": ""}),
                "max_ctx": ("INT", {"default": 512, "min": 300, "max": 100000, "step": 64}),
                "gpu_layers": ("INT", {"default": 41, "min": 0, "max": 100, "step": 1}),
                "n_threads": ("INT", {"default": 16, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_llama_checkpoint"

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def load_llama_checkpoint(self, model_name, model_path, max_ctx, gpu_layers, n_threads):
        from llama_cpp import Llama

        if model_path != "":
            model_name = ""
        if model_name in config_key:
            model_path = config_key[model_name].get("model_path")
        model = Llama(
            model_path=model_path, chat_format="llama-2", n_ctx=max_ctx, n_threads=n_threads, n_gpu_layers=gpu_layers
        )
        return (model,)


NODE_CLASS_MAPPINGS = {
    "LLM": LLM,
    "LLM_local": LLM_local,
    "LLM_api_loader": LLM_api_loader,
    "LLM_local_loader": LLM_local_loader,
    "LLavaLoader": LLavaLoader,
    "llama_guff_loader": llama_guff_loader,
    "load_embeddings": load_embeddings,
    "load_file": load_file,
    "load_persona": load_persona,
    "classify_persona": classify_persona,
    "classify_function": classify_function,
    "classify_persona_plus": classify_persona_plus,
    "classify_function_plus": classify_function_plus,
    "tool_combine": tool_combine,
    "tool_combine_plus": tool_combine_plus,
    "time_tool": time_tool,
    "weather_tool": weather_tool,
    "accuweather_tool": accuweather_tool,
    "google_tool": google_tool,
    "bing_tool": bing_tool,
    "check_web_tool": check_web_tool,
    "file_combine": file_combine,
    "file_combine_plus": file_combine_plus,
    "start_dialog": start_dialog,
    "end_dialog": end_dialog,
    "interpreter_tool": interpreter_tool,
    "ebd_tool": ebd_tool,
    "custom_persona": custom_persona,
    "start_workflow": start_workflow,
    "end_workflow": end_workflow,
    "new_interpreter_tool": new_interpreter_tool,
    "CLIPTextEncode_party": CLIPTextEncode_party,
    "KSampler_party": KSampler_party,
    "VAEDecode_party": VAEDecode_party,
    "string_logic": string_logic,
    "show_text_party": show_text_party,
    "load_url": load_url,
    "load_file_folder": load_file_folder,
    "api_tool": api_tool,
    "wikipedia_tool": wikipedia_tool,
    "load_wikipedia": load_wikipedia,
    "arxiv_tool": arxiv_tool,
    "workflow_transfer": workflow_transfer,
    "About_us": About_us,
    "workflow_tool": workflow_tool,
    "github_tool": github_tool,
    "work_wechat_tool": work_wechat_tool,
    "work_wechat": work_wechat,
    "Dingding_tool": Dingding_tool,
    "Dingding": Dingding,
    "feishu_tool": feishu_tool,
    "feishu": feishu,
    "substring": substring,
    "openai_tts": openai_tts,
    "play_audio": play_audio,
    "load_name": load_name,
    "omost_decode": omost_decode,
    "omost_setting": omost_setting,
    "keyword_tool": keyword_tool,
    "load_keyword": load_keyword,
    "listen_audio": listen_audio,
    "openai_whisper": openai_whisper,
    "story_json_tool": story_json_tool,
    "KG_json_toolkit_developer": KG_json_toolkit_developer,
    "KG_json_toolkit_user": KG_json_toolkit_user,
    "KG_csv_toolkit_developer": KG_csv_toolkit_developer,
    "KG_csv_toolkit_user": KG_csv_toolkit_user,
    "replace_string": replace_string,
    "CosyVoice": CosyVoice,
    "KG_neo_toolkit_developer": KG_neo_toolkit_developer,
    "KG_neo_toolkit_user": KG_neo_toolkit_user,
    "translate_persona": translate_persona,
    "load_excel": load_excel,
    "text_iterator": text_iterator,
    "image_iterator": image_iterator,
    "google_loader": google_loader,
    "bing_loader": bing_loader,
    "api_function": api_function,
    "parameter_function": parameter_function,
    "get_string": get_string,
    "parameter_combine": parameter_combine,
    "parameter_combine_plus": parameter_combine_plus,
    "list_append": list_append,
    "list_append_plus": list_append_plus,
    "list_extend": list_extend,
    "list_extend_plus": list_extend_plus,
    "clear_model": clear_model,
    "save_ebd_database":save_ebd_database,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "LLM": "API大语言模型(LLM_api)",
    "LLM_local": "本地大语言模型(LLM_local)",
    "LLM_api_loader": "API大语言模型加载器(LLM_api_loader)",
    "LLM_local_loader": "本地大语言模型加载器(LLM_local_loader)",
    "LLavaLoader": "LVM加载器(LVM_Loader)",
    "llama_guff_loader": "llama-guff加载器(llama_guff_loader)",
    "load_embeddings": "词嵌入模型加载器(embeddings_Loader)",
    "load_file": "加载文件(load_file)",
    "load_persona": "加载人格面具(load_persona)",
    "classify_persona": "分类器面具(classify_persona)",
    "classify_function": "分类器函数(classify_function)",
    "classify_persona_plus": "超大分类器面具(classify_persona_plus)",
    "classify_function_plus": "超大分类器函数(classify_function_plus)",
    "tool_combine": "工具组合(tool_combine)",
    "tool_combine_plus": "超大工具组合(tool_combine_plus)",
    "time_tool": "时间工具(time_tool)",
    "weather_tool": "天气工具(weather_tool)",
    "accuweather_tool": "accuweather工具(accuweather_tool)",
    "google_tool": "谷歌搜索工具(google_tool)",
    "bing_tool": "必应搜索工具(bing_tool)",
    "check_web_tool": "检视网页工具(check_web_tool)",
    "file_combine": "文件组合(file_combine)",
    "file_combine_plus": "超大文件组合(file_combine_plus)",
    "start_dialog": "开始对话(start_dialog)",
    "end_dialog": "结束对话(end_dialog)",
    "interpreter_tool": "解释器工具(interpreter_tool)",
    "ebd_tool": "词嵌入模型工具(embeddings_tool)",
    "custom_persona": "自定义面具(custom_persona)",
    "start_workflow": "开始工作流(start_workflow)",
    "end_workflow": "结束工作流(end_workflow)",
    "new_interpreter_tool": "(危险！)万能解释器工具(danger!)(omnipotent_interpreter_tool)",
    "CLIPTextEncode_party": "CLIP文本编码器(CLIPTextEncode_party)",
    "KSampler_party": "KSampler采样器(KSampler_party)",
    "VAEDecode_party": "VAEDecode解码器(VAEDecode_party)",
    "string_logic": "字符串逻辑(string_logic)",
    "show_text_party": "显示文本(show_text)",
    "load_url": "加载网页内容(load_url_content)",
    "load_file_folder": "加载文件夹(load_file_folder)",
    "api_tool": "API工具(api_tool)",
    "wikipedia_tool": "维基百科工具(wikipedia_tool)",
    "load_wikipedia": "加载维基百科(load_wikipedia)",
    "arxiv_tool": "arxiv工具(arxiv_tool)",
    "workflow_transfer": "工作流中转器(workflow_transfer)",
    "About_us": "关于我们(About_us)",
    "workflow_tool": "工作流工具(workflow_tool)",
    "github_tool": "GitHub工具(github_tool)",
    "work_wechat_tool": "企业微信工具(work_wechat_tool)",
    "work_wechat": "发送到企业微信(send_to_work_wechat)",
    "Dingding_tool": "钉钉工具(Dingding_tool)",
    "Dingding": "发送到钉钉(send_to_dingding)",
    "feishu_tool": "飞书工具(feishu_tool)",
    "feishu": "发送到飞书(send_to_feishu)",
    "substring": "提取字符串(extract_substring)",
    "openai_tts": "OpenAI语音合成(openai_tts)",
    "play_audio": "播放音频(play_audio)",
    "load_name": "加载模型名称(load_model_name)",
    "omost_decode": "omost解码器(omost_decode)",
    "omost_setting": "omost设置(omost_setting)",
    "keyword_tool": "搜索关键词工具(search_keyword_tool)",
    "load_keyword": "加载关键词检索器(load_keyword_searcher)",
    "listen_audio": "监听音频(listen_audio)",
    "openai_whisper": "OpenAI语音识别(openai_whisper)",
    "story_json_tool": "故事JSON工具(story_json_tool)",
    "KG_json_toolkit_developer": "知识图谱JSON工具包开发者版(KG_json_toolkit_developer)",
    "KG_json_toolkit_user": "知识图谱JSON工具包用户版(KG_json_toolkit_user)",
    "KG_csv_toolkit_developer": "知识图谱CSV工具包开发者版(KG_csv_toolkit_developer)",
    "KG_csv_toolkit_user": "知识图谱CSV工具包用户版(KG_csv_toolkit_user)",
    "replace_string": "替换字符串(replace_string)",
    "CosyVoice": "CosyVoice语音合成(CosyVoice)",
    "KG_neo_toolkit_developer": "知识图谱Neo4j工具包开发者版(KG_neo4j_toolkit_developer)",
    "KG_neo_toolkit_user": "知识图谱Neo4j工具包用户版(KG_neo4j_toolkit_user)",
    "translate_persona": "翻译面具(translate_persona)",
    "load_excel": "Excel迭代器(Excel_iterator)",
    "text_iterator": "文本迭代器(text_iterator)",
    "image_iterator": "图片迭代器(image_iterator)",
    "google_loader": "Google搜索加载器(Google_image_loader)",
    "bing_loader": "Bing搜索加载器(Bing_image_loader)",
    "api_function": " API函数(api_function)",
    "parameter_function": "参数字典函数(parameter_function)",
    "get_string": "获取字符串(get_string)",
    "parameter_combine": "参数字典组合(parameter_combine)",
    "parameter_combine_plus": "超大参数字典组合(parameter_combine_plus)",
    "list_append": "列表追加(list_append)",
    "list_append_plus": "超大列表追加(list_append_plus)",
    "list_extend": "列表扩展(list_extend)",
    "list_extend_plus": "超大列表扩展(list_extend_plus)",
    "clear_model": "清空模型(clear_model)",
    "save_ebd_database":" 保存向量数据库(save_ebd_database)",
}


def load_custom_tools():
    # 获取 custom_tool 文件夹的路径
    custom_tool_dir = os.path.join(os.path.dirname(__file__), "custom_tool")

    # 找到 custom_tool 文件夹下所有的 .py 文件
    files = glob.glob(os.path.join(custom_tool_dir, "*.py"), recursive=False)

    for file in files:
        # 获取文件名（不包含扩展名）
        name = os.path.splitext(os.path.basename(file))[0]

        try:
            # 创建一个导入规范
            spec = importlib.util.spec_from_file_location(name, file)

            # 根据导入规范创建一个新的模块对象
            module = importlib.util.module_from_spec(spec)

            # 在 sys.modules 中注册这个模块
            sys.modules[name] = module

            # 执行模块的代码，实际加载模块
            spec.loader.exec_module(module)

            # 如果模块有 NODE_CLASS_MAPPINGS 属性，更新字典
            if hasattr(module, "NODE_CLASS_MAPPINGS"):
                NODE_CLASS_MAPPINGS.update(getattr(module, "NODE_CLASS_MAPPINGS", {}))

            # 如果模块有 NODE_DISPLAY_NAME_MAPPINGS 属性，更新字典
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                NODE_DISPLAY_NAME_MAPPINGS.update(getattr(module, "NODE_DISPLAY_NAME_MAPPINGS", {}))

            # 如果模块有 _TOOL_HOOKS 属性，将其字符串添加到 _TOOL_HOOKS 列表中
            if hasattr(module, "_TOOL_HOOKS"):
                _TOOL_HOOKS.extend(getattr(module, "_TOOL_HOOKS", []))

                # 对于每个工具名称，将同名的函数导入到全局变量中
                for tool_name in getattr(module, "_TOOL_HOOKS", []):
                    if hasattr(module, tool_name):
                        # 将函数添加到全局变量中
                        globals()[tool_name] = getattr(module, tool_name)

        except Exception as e:
            # 处理导入错误（例如，跳过文件）
            print(f"导入 {name} 时出错：{e}")


# 调用函数来加载 custom_tool 文件夹下的模块
load_custom_tools()


if __name__ == "__main__":
    llm = LLM()
    res = llm.chatbot(
        "你好", "你是一个强大的人工智能助手。", "gpt-3.5-turbo", 0.7, tools=time_tool().time("Asia/Shanghai")
    )
