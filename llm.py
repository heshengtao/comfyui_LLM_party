import base64
import datetime
import gc
import glob
import hashlib
import importlib
import io
import json
import locale
import os
import random
import re
import sys
import time
import traceback
import google.generativeai as genai
import numpy as np
import openai
import requests
import torch
from PIL import Image
from transformers import (
    AutoModel,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM, 
    AutoModelForSequenceClassification,
    AutoTokenizer,
    GenerationConfig,
    AutoConfig,
)
import PIL.Image
if torch.cuda.is_available():
    from transformers import BitsAndBytesConfig
from google.protobuf.struct_pb2 import Struct
from torchvision.transforms import ToPILImage

from .config import config_key, config_path, current_dir_path, load_api_keys
from .tools.lorebook import Lorebook
from .tools.api_tool import (
    api_function,
    api_tool,
    json2text,
    list_append,
    list_append_plus,
    list_extend,
    list_extend_plus,
    parameter_combine,
    parameter_combine_plus,
    parameter_function,
    use_api_tool,
)
from .tools.check_web import check_web, check_web_tool
from .tools.classify_function import classify_function, classify_function_plus
from .tools.classify_persona import classify_persona, classify_persona_plus
from .tools.clear_file import clear_file
from .tools.clear_model import clear_model
from .tools.custom_persona import custom_persona
from .tools.dialog import end_dialog, start_dialog,start_anything,end_anything
from .tools.dingding import Dingding, Dingding_tool, send_dingding
from .tools.end_work import end_workflow, img2path
from .tools.excel import image_iterator, load_excel,json_iterator
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
from .tools.interpreter import interpreter, interpreter_function, interpreter_tool
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
from .tools.load_ebd import data_base, ebd_tool, embeddings_function, save_ebd_database,load_ebd
from .tools.load_file import (
    load_file,
    load_file_folder,
    load_img_path,
    load_url,
    start_workflow,
)
from .tools.load_model_name import load_name
from .tools.load_persona import load_persona
from .tools.logic import get_string, replace_string, string_logic, substring
from .tools.omost import omost_decode, omost_setting
from .tools.search_web import (
    bing_loader,
    bing_tool,
    google_loader,
    google_tool,
    search_web,
    search_web_bing,
    duckduckgo_tool,
    duckduckgo_loader,
    search_duckduckgo,
)
from .tools.show_text import About_us, show_text_party
from .tools.smalltool import bool_logic, load_int, none2false,str2float,str2int,any2str
from .tools.story import read_story_json, story_json_tool
from .tools.text_iterator import text_iterator,text_writing
from .tools.tool_combine import tool_combine, tool_combine_plus
from .tools.translate_persona import translate_persona
from .tools.tts import openai_tts
from .tools.wechat import send_wechat, work_wechat, work_wechat_tool
from .tools.wikipedia import get_wikipedia, load_wikipedia, wikipedia_tool
from .tools.workflow import work_flow, workflow_tool, workflow_transfer
from .tools.flux_persona import flux_persona
from .tools.workflow_V2 import workflow_transfer_v2
_TOOL_HOOKS = [
    "get_time",
    "get_weather",
    "search_web",
    "search_web_bing",
    "check_web",
    "interpreter",
    "data_base",
    "another_llm",
    "use_api_tool",
    "get_accuweather",
    "get_wikipedia",
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
    "search_duckduckgo",
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
            is_enable,
            extra_parameters,
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
            is_enable,
            extra_parameters,
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
            is_enable,
            extra_parameters,
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
            is_enable,
            extra_parameters,
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
        if isinstance(ret_out, tuple):
            ret = ret_out[0]
            global image_buffer
            image_buffer = ret_out[1]
            if ret == "" or ret is None:
                ret = "图片已生成。并以展示在本节点的image输出中。可以使用preview_image节点查看图片。"
        else:
            ret = ret_out
    except:
        ret = traceback.format_exc()
    return str(ret)
def convert_to_gemini(openai_history):
    for entry in openai_history:
        role = entry["role"]
        if role == "system":
            content = entry["content"]
            return content
    return ""

def convert_tool_to_gemini(openai_tools):
    gemini_tools = []
    for tool in openai_tools:
        gemini_tool = {
            "name": tool["function"]["name"],
            "description": tool["function"]["description"],
            "parameters": {
                "type": "OBJECT",
                "properties": {}
            }
        }
        for prop_name, prop_details in tool["function"]["parameters"]["properties"].items():
            gemini_tool["parameters"]["properties"][prop_name] = {
                "type": prop_details["type"].upper(),
                "description": prop_details["description"]
            }
        gemini_tool["parameters"]["required"] = tool["function"]["parameters"]["required"]
        gemini_tools.append(gemini_tool)
    return gemini_tools

class genChat:
    def __init__(self, model_name, apikey) -> None:
        self.model_name = model_name
        self.apikey = apikey

    def send(
        self,
        user_prompt,
        temperature,
        max_length,
        history,
        tools=None,
        is_tools_in_sys_prompt="disable",
        images=None,
        imgbb_api_key="",
        **extra_parameters,
    ):
        try:
            if tools is None:
                tools = []
            # Function to convert OpenAI history to Gemini history
            System_prompt= convert_to_gemini(history)
            if images is not None:
                i = 255.0 * images[0].cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                new_message = {"role": "user", "parts": [{"text": user_prompt},{"inline_data": img}]}
            else:
                new_message = {"role": "user", "parts": [{"text": user_prompt}]}
            
            history.append(new_message)
            tools = convert_tool_to_gemini(tools)
            genai.configure(api_key=self.apikey)
            tool_list={
                'function_declarations':  tools
            }
            if "n" in extra_parameters:
                extra_parameters["candidate_count"]= extra_parameters["n"]
                del extra_parameters["n"]
            # 如果extra_parameters["response_format"]存在就删除它
            if "response_format" in extra_parameters:
                del extra_parameters["response_format"]
                model = genai.GenerativeModel(self.model_name,tools=tool_list,system_instruction=System_prompt,generation_config={"response_mime_type": "application/json"})
            else:
                model = genai.GenerativeModel(self.model_name,tools=tool_list,system_instruction=System_prompt)
            response = model.generate_content(
                contents= history[1:],
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_length,
                    **extra_parameters
                }
            )
            if images is not None:
                # 移除包含 "inline_data" 的部分
                for message in history:
                    if "parts" in message:
                        message["parts"] = [part for part in message["parts"] if "inline_data" not in part]

            while response.candidates[0].content.parts[0].function_call:
                function_call =response.candidates[0].content.parts[0].function_call
                name = function_call.name
                args = {key:value for key, value in function_call.args.items()}
                res={"role": "model", "parts": response.candidates[0].content.parts}
                history.append(res)
                print("正在调用" + name + "工具")
                results = dispatch_tool(name, args)
                
                s = Struct()
                s.update({"result": results})

                function_response = genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(name=name, response=s)
                )
                res={
                    "role": "user",
                    "parts": [function_response]
                }
                print("调用结果：" + str(results))
                history.append(res)
                response = model.generate_content(
                    contents= history[1:],
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_length,
                        **extra_parameters
                    }
                )
                # 移除history最后两个元素
                history.pop()
                history.pop()
            text = response.candidates[0].content.parts[0].text
            res={"role": "model", "parts": [{"text": text}]}
            history.append(res)
        except Exception as e:
            return str(e), history
        return text, history


class Chat:
    def __init__(self, model_name, apikey, baseurl) -> None:
        self.model_name = model_name
        self.apikey = apikey
        self.baseurl = baseurl

    def send(
        self,
        user_prompt,
        temperature,
        max_length,
        history,
        tools=None,
        is_tools_in_sys_prompt="disable",
        images=None,
        imgbb_api_key="",
        **extra_parameters,
    ):
        try:
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
            if "o1" in self.model_name:
                # 将history中的系统提示词部分的角色换成user
                for i in range(len(history)):
                    if history[i]["role"] == "system":
                        history[i]["role"] = "user"
                        history.append({"role": "assistant", "content": "好的，我会按照你的指示来操作"})
                        break
            openai.api_key = self.apikey
            openai.base_url = self.baseurl
            new_message = {"role": "user", "content": user_prompt}
            history.append(new_message)
            print(history)
            if "o1" in self.model_name:
                if tools is not None:
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=history,
                        tools=tools,
                        **extra_parameters,
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
                        response = openai.chat.completions.create(
                            model=self.model_name,
                            messages=history,
                            tools=tools,
                            **extra_parameters,
                        )
                        print(response)
                elif is_tools_in_sys_prompt == "enable":
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=history,
                        **extra_parameters,
                    )
                    response_content = response.choices[0].message.content
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
                            model=self.model_name,
                            messages=history,
                            **extra_parameters,
                        )
                        response_content = response.choices[0].message.content
                else:
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=history,
                        **extra_parameters,
                    )
                    print(response)
            elif tools is not None:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=history,
                    temperature=temperature,
                    tools=tools,
                    max_tokens=max_length,
                    **extra_parameters,
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
                            **extra_parameters,
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
                            **extra_parameters,
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
                        **extra_parameters,
                    )
                response_content = response.choices[0].message.content
                print(response)
            elif is_tools_in_sys_prompt == "enable":
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=history,
                    temperature=temperature,
                    max_tokens=max_length,
                    **extra_parameters,
                )
                response_content = response.choices[0].message.content
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
                        model=self.model_name,
                        messages=history,
                        temperature=temperature,
                        max_tokens=max_length,
                        **extra_parameters,
                    )
                    response_content = response.choices[0].message.content
            else:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=history,
                    temperature=temperature,
                    max_tokens=max_length,
                    **extra_parameters,
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
                "model_name": ("STRING", {"default": "gpt-4o-mini"}),
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
                "is_ollama": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型加载器（loader）"

    def chatbot(self, model_name, base_url=None, api_key=None, is_ollama=False):
        if is_ollama:
            openai.api_key = "ollama"
            openai.base_url = "http://127.0.0.1:11434/v1/"
        else:
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
                return ("请输入API_KEY",)
            if openai.base_url != "":
                if openai.base_url[-1] != "/":
                    openai.base_url = openai.base_url + "/"

        chat = Chat(model_name, openai.api_key, openai.base_url)
        return (chat,)
llm_api_keys = load_api_keys(config_path)
llm_api_key=llm_api_keys.get("openai_api_key").strip()
llm_base_url=llm_api_keys.get("base_url").strip()
if llm_api_key == "" or llm_api_key =="sk-XXXXX" or llm_base_url == "":
    models_dict =[]
else:
    try:
        client = openai.OpenAI(api_key=llm_api_key, base_url=llm_base_url)
        models_response = client.models.list()
        # 将模型列表转换为字典
        models_dict = [model.id for model in models_response.data]
        openai.api_key=llm_api_key
        openai.base_url=llm_base_url
    except Exception as e:
        models_dict = []
class easy_LLM_api_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": (models_dict, {"default": "gpt-4o-mini"}),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型加载器（loader）"

    def chatbot(self, model_name):
        # 如果openai.base_url没有/结尾就加一个
        if openai.base_url != "":
            if openai.base_url[-1] != "/":
                openai.base_url = openai.base_url + "/"
        chat = Chat(model_name, openai.api_key, openai.base_url)
        return (chat,)

class genai_api_loader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "gemini-1.5-flash-latest"}),
            },
            "optional": {
                "api_key": (
                    "STRING",
                    {
                        "default": "",
                    },
                ),
            },
        }

    RETURN_TYPES = ("CUSTOM",)
    RETURN_NAMES = ("model",)

    FUNCTION = "chatbot"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型加载器（loader）"

    def chatbot(self, model_name, api_key=None):
        api_keys = load_api_keys(config_path)
        if api_key != "":
            api_key = api_key
        elif model_name in config_key:
            api_keys = config_key[model_name]
            api_key = api_keys.get("api_key")
        elif api_keys.get("openai_api_key") != "":
            api_key = api_keys.get("openai_api_key")
        if api_key == "":
            return ("请输入API_KEY",)

        chat = genChat(model_name, api_key)
        return (chat,)

class LLM:
    def __init__(self):
        current_time = datetime.datetime.now()
        # 以时间戳作为ID，字符串格式 XX年XX月XX日XX时XX分XX秒并加上一个哈希值防止重复
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
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
                "max_length": ("INT", {"default": 1920, "min": 256, "max": 128000, "step": 128}),
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
                "is_enable": ("BOOLEAN", {"default": True}),
                "extra_parameters": ("DICT", {"forceInput": True}),
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
        is_enable=True,
        extra_parameters=None,
    ):
        if not is_enable:
            return (
                None,
                None,
                None,
                [],
            )
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
            is_enable,
            extra_parameters,
        ]
        if user_prompt is None:
            user_prompt = user_prompt_input
        elif user_prompt_input is not None:
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
        if (user_prompt is None or user_prompt.strip() == "") and (images is None or images == []):
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
                if is_memory == "disable" or "clear party memory" in user_prompt:
                    with open(self.prompt_path, "w", encoding="utf-8") as f:
                        json.dump([{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False)
                    if "clear party memory" in user_prompt:
                        with open(self.prompt_path, "r", encoding="utf-8") as f:
                            history = json.load(f)
                        return (
                            "party memory has been cleared, please ask me again, powered by LLM party!",
                            str(history),
                            llm_tools_json,
                            None,
                        )
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
                        tools = None
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
                if extra_parameters is not None and extra_parameters != {}:
                    response, history = model.send(
                        user_prompt, temperature, max_length, history, tools, is_tools_in_sys_prompt,images,imgbb_api_key, **extra_parameters
                    )
                else:
                    response, history = model.send(
                        user_prompt, temperature, max_length, history, tools, is_tools_in_sys_prompt,images,imgbb_api_key
                    )
                print(response)
                # 修改prompt.json文件
                history_get = [history[0]]
                history_get.extend(history_copy)
                history_get.extend(history[1:])
                history = history_get
                with open(self.prompt_path, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                history = json.dumps(history, ensure_ascii=False,indent=4)
                global image_buffer
                image_out = image_buffer
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
    def original_IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


def llm_chat(
    model, tokenizer, user_prompt, history, device, max_length, role="user", temperature=0.7, **extra_parameters
):
    history.append({"role": role, "content": user_prompt.strip()})
    # 检查是否已经设置了 chat_template
    if not hasattr(tokenizer, 'chat_template') or tokenizer.chat_template is None:
        # 如果没有设置 chat_template，尝试使用 default_chat_template
        if hasattr(tokenizer, 'default_chat_template') and tokenizer.default_chat_template is not None:
            tokenizer.chat_template = tokenizer.default_chat_template
        else:
            print("chat_template is not set")
            model_inputs = tokenizer([user_prompt.strip()], return_tensors="pt").to(device)
            generated_ids = model.generate(
                model_inputs.input_ids,
                max_new_tokens=max_length,
                do_sample=True,
                temperature=temperature,
                eos_token_id=tokenizer.eos_token_id,
                **extra_parameters,  # Add the eos_token_id parameter
            )
            response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            history.append({"role": "assistant", "content": response})
            return response, history
    text = tokenizer.apply_chat_template(history, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=max_length,
        do_sample=True,
        temperature=temperature,
        eos_token_id=tokenizer.eos_token_id,
        **extra_parameters,  # Add the eos_token_id parameter
    )
    generated_ids = [
        output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    history.append({"role": "assistant", "content": response})
    return response, history

def vlm_chat(
    model, processor, image, user_prompt, history, device, max_length, role="user", temperature=0.7, **extra_parameters
):
    if image !=[]:
        user_content = {
            "role": role,
            "content": [
                {"type": "image"},
                {"type": "text", "text": user_prompt},
            ],
        }
        history.append(user_content)
        input_text = processor.apply_chat_template(history, add_generation_prompt=True)
        inputs = processor(image, input_text, return_tensors="pt").to(device)
    else:
        user_content = {
            "role": role,
            "content": [
                {"type": "text", "text": user_prompt},
            ],
        }
        history.append(user_content)
        input_text = processor.apply_chat_template(history, add_generation_prompt=True)
        inputs = processor(text=input_text, return_tensors="pt").to(device)
    

    output = model.generate(**inputs, max_new_tokens=max_length, temperature=temperature, **extra_parameters)
    response = processor.decode(output[0], skip_special_tokens=True)
    # 使用正则表达式提取最后一个助手的回答
    matches = re.findall(r'assistant\s*(.*?)(?=\s*(?:system|user|$))', response, re.DOTALL)
    if matches:
        assistant_output = matches[-1].strip()
    else:
        assistant_output = response.strip()
    history.append({"role": "assistant", "content":assistant_output})
    
    return assistant_output, history



class LLM_local_loader:
    def __init__(self):
        self.id = hash(str(self))
        self.device = ""
        self.dtype = ""
        self.model_name_or_path = ""
        self.model = ""
        self.tokenizer = ""
        self.is_locked = False

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name_or_path": ("STRING", {"default": ""}),
                "device": (
                    ["auto", "cuda", "cpu", "mps"],
                    {
                        "default": "auto",
                    },
                ),
                "dtype": (
                    ["float32", "float16","bfloat16", "int8", "int4"],
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

    CATEGORY = "大模型派对（llm_party）/模型加载器（loader）"

    def chatbot(self, model_name_or_path, device, dtype, is_locked=True):
        self.is_locked = is_locked
        if self.is_locked == False:
            setattr(LLM_local_loader, "IS_CHANGED", LLM_local_loader.original_IS_CHANGED)
        else:
            # 如果方法存在，则删除
            if hasattr(LLM_local_loader, "IS_CHANGED"):
                delattr(LLM_local_loader, "IS_CHANGED")
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        if (
            self.device != device
            or self.dtype != dtype
            or self.model_name_or_path != model_name_or_path
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
            self.model_name_or_path = model_name_or_path
            self.device = device
            self.dtype = dtype
            model_kwargs = {
                'device_map': device,
            }

            if dtype == "float16":
                model_kwargs['torch_dtype'] = torch.float16
            elif dtype == "bfloat16":
                model_kwargs['torch_dtype'] = torch.bfloat16
            elif dtype in ["int8", "int4"]:
                model_kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4"))

            config = AutoConfig.from_pretrained(model_name_or_path, **model_kwargs)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

            if config.model_type == "t5":
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, **model_kwargs)
            elif config.model_type in ["gpt2", "gpt_refact", "gemma", "llama", "mistral", "qwen2", "chatglm"]:
                self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path, **model_kwargs)
            else:
                raise ValueError(f"Unsupported model type: {config.model_type}")
            self.model = self.model.eval()
        return (
            self.model,
            self.tokenizer,
        )

    @classmethod
    def original_IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value

LLM_dir=os.path.join(current_dir_path, "model","LLM")
# 获取LLM_dir文件夹中的所有文件夹
LLM_list = [f for f in os.listdir(LLM_dir) if os.path.isdir(os.path.join(LLM_dir, f))]
class easy_LLM_local_loader:
    def __init__(self):
        self.id = hash(str(self))
        self.device = ""
        self.dtype = ""
        self.model_name_or_path = ""
        self.model = ""
        self.tokenizer = ""
        self.is_locked = False

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name_or_path": (LLM_list, {"default": ""}),
                "device": (
                    ["auto", "cuda", "cpu", "mps"],
                    {
                        "default": "auto",
                    },
                ),
                "dtype": (
                    ["float32", "float16","bfloat16", "int8", "int4"],
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

    CATEGORY = "大模型派对（llm_party）/模型加载器（loader）"

    def chatbot(self, model_name_or_path, device, dtype, is_locked=True):
        model_name_or_path=os.path.join(LLM_dir,model_name_or_path)
        self.is_locked = is_locked
        if self.is_locked == False:
            setattr(easy_LLM_local_loader, "IS_CHANGED", easy_LLM_local_loader.original_IS_CHANGED)
        else:
            # 如果方法存在，则删除
            if hasattr(easy_LLM_local_loader, "IS_CHANGED"):
                delattr(easy_LLM_local_loader, "IS_CHANGED")
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        if (
            self.device != device
            or self.dtype != dtype
            or self.model_name_or_path != model_name_or_path
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
            self.model_name_or_path = model_name_or_path
            self.device = device
            self.dtype = dtype
            model_kwargs = {
                'device_map': device,
            }

            if dtype == "float16":
                model_kwargs['torch_dtype'] = torch.float16
            elif dtype == "bfloat16":
                model_kwargs['torch_dtype'] = torch.bfloat16
            elif dtype in ["int8", "int4"]:
                model_kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=(dtype == "int8"), load_in_4bit=(dtype == "int4"))

            config = AutoConfig.from_pretrained(model_name_or_path, **model_kwargs)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

            if config.model_type == "t5":
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, **model_kwargs)
            elif config.model_type in ["gpt2", "gpt_refact", "gemma", "llama", "mistral", "qwen2", "chatglm"]:
                self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path, **model_kwargs)
            else:
                raise ValueError(f"Unsupported model type: {config.model_type}")
            self.model = self.model.eval()
        return (
            self.model,
            self.tokenizer,
        )

    @classmethod
    def original_IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value


class LLM_local:
    def __init__(self):
        # 生成一个hash值作为id
        current_time = datetime.datetime.now()
        self.id = current_time.strftime("%Y_%m_%d_%H_%M_%S") + str(hash(random.randint(0, 1000000)))
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
        self.images = []

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
                    ["LLM","LLM-GGUF", "VLM-GGUF", "VLM(testing)"],
                    {
                        "default": "LLM",
                    },
                ),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_length":("INT", {"default": 512, "min": 256, "max": 128000, "step": 128}),
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
                "is_enable": ("BOOLEAN", {"default": True}),
                "extra_parameters": ("DICT", {"forceInput": True}),
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
        is_enable=True,
        extra_parameters=None,
    ):
        if not is_enable:
            return (
                None,
                None,
                None,
                [],
            )
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
            is_enable,
            extra_parameters,
        ]
        if user_prompt is None:
            user_prompt = user_prompt_input
        elif user_prompt_input is not None:
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
        if (user_prompt is None or user_prompt.strip() == "") and (image is None or image == []):
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            return (
                "",
                str(history),
                llm_tools_json,
            )
        else:
            try:
                if is_memory == "disable" or "clear party memory" in user_prompt:
                    self.images= []
                    with open(self.prompt_path, "w", encoding="utf-8") as f:
                        json.dump([{"role": "system", "content": system_prompt}], f, indent=4, ensure_ascii=False)
                    if "clear party memory" in user_prompt:
                        with open(self.prompt_path, "r", encoding="utf-8") as f:
                            history = json.load(f)
                        return (
                            "party memory has been cleared, please ask me again, powered by LLM party!",
                            str(history),
                            llm_tools_json,
                            None,
                        )
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
                            if model_type == "GLM3":
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
                if model_type not in ["VLM-GGUF", "LLM-GGUF"]:
                    device = next(model.parameters()).device
                if model_type == "LLM":
                    if extra_parameters is not None and extra_parameters != {}:
                        response, history = llm_chat(
                            model,
                            tokenizer,
                            user_prompt,
                            history,
                            device,
                            max_length,
                            temperature=temperature,
                            **extra_parameters,
                        )
                    else:
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
                        if extra_parameters is not None and extra_parameters != {}:
                            response, history = llm_chat(
                                model,
                                tokenizer,
                                results,
                                history,
                                device,
                                max_length,
                                role="tool",
                                temperature=temperature,
                                **extra_parameters,
                            )
                        else:
                            response, history = llm_chat(
                                model,
                                tokenizer,
                                results,
                                history,
                                device,
                                max_length,
                                role="tool",
                                temperature=temperature,
                            )
                elif model_type == "VLM-GGUF":
                    if image is not None:
                        pil_image = ToPILImage()(image[0].permute(2, 0, 1))
                        # Convert the PIL image to a bytes buffer
                        buffer = io.BytesIO()
                        pil_image.save(buffer, format="PNG")  # You can change the format if needed
                        # Encode the bytes to base64
                        base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
                        user_content = {
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_string}"}},
                                {"type": "text", "text": user_prompt},
                            ],
                        }
                        history.append(user_content)
                        if extra_parameters is not None and extra_parameters != {}:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                                **extra_parameters,
                            )
                        else:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                            )
                        response = f"{response['choices'][0]['message']['content']}"
                        print(response)
                        assistant_content = {"role": "assistant", "content": response}
                        history.append(assistant_content)
                    else:
                        user_content = {"role": "user", "content": user_prompt}
                        history.append(user_content)
                        if extra_parameters is not None and extra_parameters != {}:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                                **extra_parameters,
                            )
                        else:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                            )
                        response = f"{response['choices'][0]['message']['content']}"
                        assistant_content = {"role": "assistant", "content": response}
                        history.append(assistant_content)
                elif model_type == "LLM-GGUF":
                    user_content = {"role": "user", "content": user_prompt}
                    history.append(user_content)
                    if extra_parameters is not None and extra_parameters != {}:
                        response = model.create_chat_completion(
                            messages=history,
                            temperature=temperature,
                            max_tokens=max_length,
                            tools=tools,
                            **extra_parameters,
                        )
                    else:
                        response = model.create_chat_completion(
                            messages=history,
                            temperature=temperature,
                            max_tokens=max_length,
                            tools=tools,
                        )
                    assistant_message = f"{response['choices'][0]['message']['content']}"
                    while assistant_message.startswith('{"name":'):
                        response_content = json.loads(assistant_message)
                        print("正在调用" + response_content['name'] + "工具")
                        results = dispatch_tool(response_content['name'], response_content['parameters'])
                        print(results)
                        assistant_content = {"role": "assistant", "content": assistant_message}
                        history.append(assistant_content)    
                        history.append(
                            {
                                "role": "function_call",
                                "content": results,
                            }
                        )
                        if extra_parameters is not None and extra_parameters != {}:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                                tools=tools,
                                **extra_parameters,
                            )
                        else:
                            response = model.create_chat_completion(
                                messages=history,
                                temperature=temperature,
                                max_tokens=max_length,
                                tools=tools,
                            )
                        print(response)   
                        assistant_message = f"{response['choices'][0]['message']['content']}"
                    assistant_content = {"role": "assistant", "content": assistant_message}
                    response= assistant_message
                    history.append(assistant_content)    
                elif model_type =="VLM(testing)":
                    if image is not None:
                        pil_image = ToPILImage()(image[0].permute(2, 0, 1))
                        self.images.append(pil_image)
                    if extra_parameters is not None and extra_parameters != {}:
                        response, history = vlm_chat(
                            model,
                            tokenizer,
                            self.images,
                            user_prompt,
                            history,
                            device,
                            max_length,
                            temperature=temperature,
                            **extra_parameters,
                        )
                    else:
                        response, history = vlm_chat(
                            model, tokenizer, self.images, user_prompt, history, device, max_length, temperature=temperature
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
                        if extra_parameters is not None and extra_parameters != {}:
                            response, history = vlm_chat(
                                model,
                                tokenizer,
                                self.images, # image,
                                results,
                                history,
                                device,
                                max_length,
                                role="tool",
                                temperature=temperature,
                                **extra_parameters,
                            )
                        else:
                            response, history = vlm_chat(
                                model,
                                tokenizer,
                                self.images, # image,
                                results,
                                history,
                                device,
                                max_length,
                                role="tool",
                                temperature=temperature,
                            )         
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
                image_out = image_buffer
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
    def original_IS_CHANGED(s):
        # 生成当前时间的哈希值
        hash_value = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()
        return hash_value




NODE_CLASS_MAPPINGS = {
    "LLM": LLM,
    "LLM_local": LLM_local,
    "LLM_api_loader": LLM_api_loader,
    "genai_api_loader":genai_api_loader,
    "LLM_local_loader": LLM_local_loader,
    "easy_LLM_local_loader": easy_LLM_local_loader,
    "easy_LLM_api_loader":easy_LLM_api_loader,
    "load_ebd":load_ebd,
    "load_file": load_file,
    "load_persona": load_persona,
    "embeddings_function": embeddings_function,
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
    "load_name": load_name,
    "omost_decode": omost_decode,
    "omost_setting": omost_setting,
    "keyword_tool": keyword_tool,
    "load_keyword": load_keyword,
    "story_json_tool": story_json_tool,
    "KG_json_toolkit_developer": KG_json_toolkit_developer,
    "KG_json_toolkit_user": KG_json_toolkit_user,
    "KG_csv_toolkit_developer": KG_csv_toolkit_developer,
    "KG_csv_toolkit_user": KG_csv_toolkit_user,
    "replace_string": replace_string,
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
    "save_ebd_database": save_ebd_database,
    "json2text": json2text,
    "interpreter_function": interpreter_function,
    "load_img_path": load_img_path,
    "img2path": img2path,
    "load_int": load_int,
    "none2false": none2false,
    "bool_logic": bool_logic,
    "duckduckgo_tool":duckduckgo_tool,
    "duckduckgo_loader":duckduckgo_loader,
    "flux_persona":flux_persona,
    "clear_file":clear_file,
    "workflow_transfer_v2":workflow_transfer_v2,
    "str2float":str2float,
    "json_iterator":json_iterator,
    "Lorebook":Lorebook,
    "text_writing":text_writing,
    "str2int":str2int,
    "any2str":any2str,
    "start_anything":start_anything,
    "end_anything":end_anything,
}


lang = locale.getdefaultlocale()[0]
api_keys = load_api_keys(config_path)
lang_config=api_keys.get("language")
if lang_config=="en_US" or lang_config=="zh_CN":
    lang=lang_config
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLM": "API LLM通用链路",
        "LLM_local": "本地LLM通用链路",
        "LLM_api_loader": "API 模型加载器",
        "easy_LLM_api_loader": "简易API 模型加载器",
        "genai_api_loader":"Gemini API 模型加载器",
        "LLM_local_loader": "本地模型加载器",
        "easy_LLM_local_loader": "简易本地模型加载器",
        "load_ebd": "加载词嵌入",
        "embeddings_function": "词向量检索",
        "load_file": "加载文件",
        "load_persona": "加载人格面具",
        "classify_persona": "分类器面具",
        "classify_function": "分类器函数",
        "classify_persona_plus": "超大分类器面具",
        "classify_function_plus": "超大分类器函数",
        "tool_combine": "工具组合",
        "tool_combine_plus": "超大工具组合",
        "time_tool": "时间工具",
        "weather_tool": "天气工具",
        "accuweather_tool": "accuweather工具",
        "google_tool": "谷歌搜索工具",
        "bing_tool": "必应搜索工具",
        "check_web_tool": "检视网页工具",
        "file_combine": "文件组合",
        "file_combine_plus": "超大文件组合",
        "start_dialog": "开始对话",
        "end_dialog": "结束对话",
        "interpreter_tool": "解释器工具",
        "ebd_tool": "词嵌入模型工具",
        "custom_persona": "自定义面具",
        "start_workflow": "开始工作流",
        "end_workflow": "结束工作流",
        "CLIPTextEncode_party": "CLIP文本编码器",
        "KSampler_party": "KSampler采样器",
        "VAEDecode_party": "VAEDecode解码器",
        "string_logic": "字符串逻辑",
        "show_text_party": "显示文本",
        "load_url": "加载网页内容",
        "load_file_folder": "加载文件夹",
        "api_tool": "API工具",
        "wikipedia_tool": "维基百科工具",
        "load_wikipedia": "加载维基百科",
        "workflow_transfer": "工作流中转器",
        "About_us": "关于我们",
        "workflow_tool": "工作流工具",
        "github_tool": "GitHub工具",
        "work_wechat_tool": "企业微信工具",
        "work_wechat": "发送到企业微信",
        "Dingding_tool": "钉钉工具",
        "Dingding": "发送到钉钉",
        "feishu_tool": "飞书工具",
        "feishu": "发送到飞书",
        "substring": "提取字符串",
        "openai_tts": "OpenAI语音合成",
        "load_name": "加载config.ini中的模型名称",
        "omost_decode": "omost解码器",
        "omost_setting": "omost设置",
        "keyword_tool": "搜索关键词工具",
        "load_keyword": "加载关键词检索器",
        "story_json_tool": "故事JSON工具",
        "KG_json_toolkit_developer": "知识图谱JSON工具包开发者版",
        "KG_json_toolkit_user": "知识图谱JSON工具包用户版",
        "KG_csv_toolkit_developer": "知识图谱CSV工具包开发者版",
        "KG_csv_toolkit_user": "知识图谱CSV工具包用户版",
        "replace_string": "替换字符串",
        "KG_neo_toolkit_developer": "知识图谱Neo4j工具包开发者版",
        "KG_neo_toolkit_user": "知识图谱Neo4j工具包用户版",
        "translate_persona": "翻译面具",
        "load_excel": "Excel迭代器",
        "text_iterator": "文本迭代器",
        "image_iterator": "图片迭代器",
        "google_loader": "Google搜索加载器",
        "bing_loader": "Bing搜索加载器",
        "api_function": "API函数",
        "parameter_function": "参数字典函数",
        "get_string": "输入字符串",
        "parameter_combine": "参数字典组合",
        "parameter_combine_plus": "超大参数字典组合",
        "list_append": "列表追加",
        "list_append_plus": "超大列表追加",
        "list_extend": "列表扩展",
        "list_extend_plus": "超大列表扩展",
        "clear_model": "清空模型",
        "save_ebd_database": "保存向量数据库",
        "json2text": "JSON转文本",
        "interpreter_function": "解释器函数",
        "load_img_path": "从图片路径加载",
        "img2path": "图片存至路径",
        "load_int": "加载整数",
        "none2false": "None转False",
        "bool_logic": "布尔逻辑",
        "duckduckgo_tool": "DuckDuckGo工具",
        "duckduckgo_loader": "DuckDuckGo加载器",
        "flux_persona":"flux提示词生成器面具",
        "clear_file":"清理文件",
        "workflow_transfer_v2":"工作流中转器V2",
        "str2float":"字符串转浮点数",
        "json_iterator":"JSON迭代器",
        "Lorebook":"Lorebook传说书",
        "text_writing":"文本写入",
        "str2int":"字符串转整数",
        "any2str":"任意类型转字符串",
        "start_anything":"开始任意",
        "end_anything": "结束任意",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "LLM": "API LLM general link",
        "LLM_local": "Local LLM general link",
        "LLM_api_loader": "API LLM Loader",
        "easy_LLM_api_loader": "Easy API LLM Loader",
        "genai_api_loader":"Gemini API LLM Loader",
        "LLM_local_loader": "Local LLM Loader",
        "easy_LLM_local_loader": "Easy Local LLM Loader",
        "load_ebd": "Load Embeddings",
        "embeddings_function": "Word Vector Search",
        "load_file": "Load File",
        "load_persona": "Load Persona",
        "classify_persona": "Classify Persona",
        "classify_function": "Classify Function",
        "classify_persona_plus": "Large Classify Persona",
        "classify_function_plus": "Large Classify Function",
        "tool_combine": "Tool Combine",
        "tool_combine_plus": "Large Tool Combine",
        "time_tool": "Time Tool",
        "weather_tool": "Weather Tool",
        "accuweather_tool": "accuweather Tool",
        "google_tool": "Google Search Tool",
        "bing_tool": "Bing Search Tool",
        "check_web_tool": "Check Web Tool",
        "file_combine": "File Combine",
        "file_combine_plus": "Large File Combine",
        "start_dialog": "Start Dialog",
        "end_dialog": "End Dialog",
        "interpreter_tool": "Interpreter Tool",
        "ebd_tool": "Embeddings Tool",
        "custom_persona": "Custom Persona",
        "start_workflow": "Start Workflow",
        "end_workflow": "End Workflow",
        "CLIPTextEncode_party": "CLIP Text Encoder",
        "KSampler_party": "KSampler",
        "VAEDecode_party": "VAEDecode",
        "string_logic": "String Logic",
        "show_text_party": "Show Text",
        "load_url": "Load URL Content",
        "load_file_folder": "Load File Folder",
        "api_tool": "API Tool",
        "wikipedia_tool": "Wikipedia Tool",
        "load_wikipedia": "Load Wikipedia",
        "workflow_transfer": "Workflow Transfer",
        "About_us": "About Us",
        "workflow_tool": "Workflow Tool",
        "github_tool": "GitHub Tool",
        "work_wechat_tool": "Work WeChat Tool",
        "work_wechat": "Send to Work WeChat",
        "Dingding_tool": "Dingding Tool",
        "Dingding": "Send to Dingding",
        "feishu_tool": "Feishu Tool",
        "feishu": "Send to Feishu",
        "substring": "Extract Substring",
        "openai_tts": "OpenAI TTS",
        "load_name": "Load Model Name in config.ini",
        "omost_decode": "omost Decoder",
        "omost_setting": "omost Setting",
        "keyword_tool": "Search Keyword Tool",
        "load_keyword": "Load Keyword Searcher",
        "story_json_tool": "Story JSON Tool",
        "KG_json_toolkit_developer": "KG JSON Toolkit Developer",
        "KG_json_toolkit_user": "KG JSON Toolkit User",
        "KG_csv_toolkit_developer": "KG CSV Toolkit Developer",
        "KG_csv_toolkit_user": "KG CSV Toolkit User",
        "replace_string": "Replace String",
        "KG_neo_toolkit_developer": "KG Neo4j Toolkit Developer",
        "KG_neo_toolkit_user": "KG Neo4j Toolkit User",
        "translate_persona": "Translate Persona",
        "load_excel": "Excel Iterator",
        "text_iterator": "Text Iterator",
        "image_iterator": "Image Iterator",
        "google_loader": "Google Image Loader",
        "bing_loader": "Bing Image Loader",
        "api_function": "API Function",
        "parameter_function": "Parameter Dictionary Function",
        "get_string": "Input String",
        "parameter_combine": "Parameter Dictionary Combine",
        "parameter_combine_plus": "Large Parameter Dictionary Combine",
        "list_append": "List Append",
        "list_append_plus": "Large List Append",
        "list_extend": "List Extend",
        "list_extend_plus": "Large List Extend",
        "clear_model": "Clear Model",
        "save_ebd_database": "Save Embeddings Database",
        "json2text": "JSON to Text",
        "interpreter_function": "Interpreter Function",
        "load_img_path": "Load Image from Path",
        "img2path": "Image to Path",
        "load_int": "Load Integer",
        "none2false": "None to False",
        "bool_logic": "Boolean Logic",
        "duckduckgo_tool": "DuckDuckGo Tool",
        "duckduckgo_loader":"DuckDuckGo Loader",
        "flux_persona":"flux prompt word generator",
        "clear_file":"clear file",
        "workflow_transfer_v2": "Workflow Transfer V2",
        "str2float": "String to Float",
        "json_iterator": "JSON Iterator",
        "Lorebook":"Lore book",
        "text_writing":"Text write",
        "str2int": "String to Integer",
        "any2str": "Any to String",
        "start_anything": "Start Anything",
        "end_anything": "End Anything",
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
    print("hello llm party!")

