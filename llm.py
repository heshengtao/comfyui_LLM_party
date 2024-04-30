import gc
import hashlib
import importlib
import json
import os
import re
import sys
import base64
from PIL import Image
import numpy as np
import io
import time
import traceback
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import openai
import requests
import torch
from .config import config_path,current_dir_path,load_api_keys
from .tools.load_file import load_file,start_workflow
from .tools.tool_combine import tool_combine,tool_combine_plus
from .tools.get_time import get_time,time_tool
from .tools.get_weather import get_weather,weather_tool
from .tools.search_web import search_web,google_tool
from .tools.check_web import check_web,check_web_tool
from .tools.file_combine import file_combine,file_combine_plus
from .tools.dialog import start_dialog,end_dialog
from .tools.interpreter import interpreter,interpreter_tool
from .tools.load_persona import load_persona
from .tools.classify_persona import classify_persona
from .tools.classify_function import classify_function
from .tools.load_ebd import ebd_tool,data_base
from .tools.custom_persona import custom_persona
from .tools.end_work import end_workflow
from .tools.new_interpreter import new_interpreter,new_interpreter_tool
from .tools.image import CLIPTextEncode_party,KSampler_party,VAEDecode_party
from transformers import AutoTokenizer, AutoModel, Qwen2Tokenizer, Qwen2ForCausalLM, AutoModelForCausalLM, GenerationConfig
glm_tokenizer=""
glm_model=""
llama_tokenizer=""
llama_model=""
qwen_tokenizer=""
qwen_model=""
_TOOL_HOOKS=[
    "get_time",
    "get_weather",
    "search_web",
    "check_web",
    "interpreter",
    "data_base",
    "another_llm",
    "new_interpreter",
]
instances=[]
def another_llm(id,type,question):
    print(id,type,question)
    global instances
    if type=="api":
        try:
            llm = next((instance for instance in instances if str(instance.id).strip() == str(id).strip()), None)
        except:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        if llm is None:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        main_brain,system_prompt,model_name,temperature,is_memory,is_tools_in_sys_prompt,is_locked,max_length,tools,file_content,api_key,base_url,images,imgbb_api_key=llm.list
        res,_,_=llm.chatbot(question,main_brain,system_prompt,model_name,temperature,is_memory,is_tools_in_sys_prompt,is_locked,max_length,tools,file_content,api_key,base_url,images,imgbb_api_key)
    elif type=="local":
        try:
            llm = next((instance for instance in instances if str(instance.id).strip() == str(id).strip()), None)
        except:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        if llm is None:
            print("找不到对应的智能助手")
            return "找不到对应的智能助手"
        main_brain,system_prompt,model_type,temperature,model_path,max_length,tokenizer_path,is_reload,device,is_memory,is_tools_in_sys_prompt,is_locked,tools,file_content=llm.list
        res,_,_=llm.chatbot(question,main_brain,system_prompt,model_type,temperature,model_path,max_length,tokenizer_path,is_reload,device,is_memory,is_tools_in_sys_prompt,is_locked,tools,file_content)
    else:
        return "type参数错误，请使用api或local"
    print(res)
    return "你调用的智能助手的问答是："+res+"\n请根据以上回答，回答用户的问题。"

llm_tools_list=[]
llm_tools=[{
    "type": "function",
    "function": {
        "name": "another_llm",
        "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："+json.dumps(llm_tools_list,ensure_ascii=False,indent=4),
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "智能助手的id"},
                "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
            },
            "required": ["id","type","question"]
        }
    }
}]
def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    if "multi_tool_use." in tool_name:
        tool_name=tool_name.replace("multi_tool_use.", "")
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = globals().get(tool_name)
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)


class Chat:
    def __init__(self, history, model_name, temperature,max_length,tools=None) -> None:
        self.messages = history
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools
        self.max_tokens=max_length

    def send(self, user_prompt):
        try:
            new_message = {"role": "user", "content": user_prompt}
            self.messages.append(new_message)
            print(self.messages)
            if self.tools is not None:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages,
                    temperature=self.temperature,
                    tools=self.tools,
                    max_tokens=self.max_tokens
                )
                while response.choices[0].message.tool_calls:
                    assistant_message=response.choices[0].message
                    response_content = assistant_message.tool_calls[0].function
                    results = dispatch_tool(response_content.name,json.loads(response_content.arguments))
                    self.messages.append({"role": assistant_message.role, "content": str(response_content)})
                    self.messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": response_content.name, "content": results})
                    response = openai.chat.completions.create(
                    model=self.model_name,  
                    messages=self.messages,
                    tools=self.tools,
                    max_tokens=self.max_tokens
                    )
                    print(response)
                while response.choices[0].message.function_call:
                    assistant_message = response.choices[0].message
                    function_call = assistant_message.function_call
                    function_name = function_call.name
                    function_arguments = json.loads(function_call.arguments)
                    results = dispatch_tool(function_name, function_arguments)
                    self.messages.append({"role": assistant_message.role, "content": str(function_call)})
                    self.messages.append({"role": "function", "name": function_name, "content": results})
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=self.messages,
                        tools=self.tools,
                        max_tokens=self.max_tokens
                    )
                response_content = response.choices[0].message.content
                print(response)
                start_pattern = "interpreter\n ```python\n"
                end_pattern = "\n```"
                while response_content.startswith(start_pattern):
                    start_index = response_content.find(start_pattern)
                    end_index = response_content.find(end_pattern)
                    if start_index != -1 and end_index != -1:
                        # 提取代码部分
                        code = response_content[start_index + len(start_pattern):end_index]
                        code = code.strip()  # 去除首尾空白字符
                    else:
                        code = ""
                    results =interpreter(code)
                    self.messages.append({"role": "function", "name": "interpreter", "content": results})
                    response = openai.chat.completions.create(
                        model=self.model_name,
                        messages=self.messages,
                        tools=self.tools,
                        max_tokens=self.max_tokens
                    )
                    response_content = response.choices[0].message.content
            else:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
            response_content = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_content})
        except Exception as ex:
            response_content = "这个话题聊太久了，我想聊点别的了：" + str(ex)
        return response_content, self.messages



class LLM:
    
    def __init__(self):
        #生成一个hash值作为id
        self.id=hash(str(self))
        global instances
        instances.append(self)
        # 构建prompt.json的绝对路径
        self.prompt_path = os.path.join(current_dir_path,"temp", str(self.id)+'.json')
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": "你是一个强大的人工智能助手。"}], f, indent=4, ensure_ascii=False)
        self.tool_data={"id":self.id,"system_prompt":"","type":"api"}
        self.list=[]
        self.added_to_list = False
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你一个强大的人工智能助手。"
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你好",
                }),
                "model_name": ("STRING", {
                    "default": "gpt-3.5-turbo-1106"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "is_memory": (["enable", "disable"],{
                    "default":"enable"
                }),
                "is_tools_in_sys_prompt": (["enable", "disable"],{
                    "default":"disable"
                }),
                "is_locked": (["enable", "disable"],{
                    "default":"disable"
                }),
                "main_brain": (["enable", "disable"],{
                    "default":"enable"
                }),
                "max_length": ("INT", {
                    "default": 2048,
                    "min": 256,
                    "step": 256
                })
            },
            "optional": {
                "tools": ("STRING", {
                    "forceInput": True
                }),
                "file_content": ("STRING", {
                    "forceInput": True
                }),
                "base_url": ("STRING", {
                    "default": "",
                }),
                "api_key": ("STRING", {
                    "default": "",
                }),
                "images": ("IMAGE", {
                    "forceInput": True
                }),
                "imgbb_api_key": ("STRING", {
                    "default": "",
                }),
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("assistant_response","history","tool",)

    FUNCTION = "chatbot"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）"

    def chatbot(self, user_prompt,main_brain ,system_prompt,model_name,temperature,is_memory,is_tools_in_sys_prompt,is_locked,max_length,tools=None,file_content=None,api_key=None,base_url=None,images=None,imgbb_api_key=None):
        self.list=[main_brain,system_prompt,model_name,temperature,is_memory,is_tools_in_sys_prompt,is_locked,max_length,tools,file_content,api_key,base_url,images,imgbb_api_key]
        self.tool_data["system_prompt"]=system_prompt
        global llm_tools_list,llm_tools
        if main_brain =="disable":
            if self.added_to_list == False:
                llm_tools_list.append(self.tool_data)
                self.added_to_list = True
        llm_tools=[{
    "type": "function",
    "function": {
        "name": "another_llm",
        "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："+json.dumps(llm_tools_list,ensure_ascii=False,indent=4),
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "智能助手的id"},
                "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
            },
            "required": ["id","type","question"]
        }
    }
}]
        
        llm_tools_json=json.dumps(llm_tools,ensure_ascii=False,indent=4)
        if user_prompt=="#清空":
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": system_prompt}], f, indent=4, ensure_ascii=False)
                            
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return ("已清空历史记录",str(history),llm_tools_json,)
        elif user_prompt is None or user_prompt.strip()=="empty":
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return ("",str(history),llm_tools_json,)
        else:
            try:
                # 读取prompt.json文件
                with open(self.prompt_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                if is_locked=="enable":
                    #返回对话历史中，最后一个content
                    return (history[-1]['content'],str(history),)
                if is_memory=="disable":
                    with open(self.prompt_path, 'w', encoding='utf-8') as f:
                        json.dump([{"role": "system","content": system_prompt}], f, indent=4, ensure_ascii=False)
                api_keys=load_api_keys(config_path)
                if api_key !="":
                    openai.api_key = api_key
                elif api_keys.get('openai_api_key')!="":
                    openai.api_key = api_keys.get('openai_api_key')
                else:
                    openai.api_key = os.environ.get("OPENAI_API_KEY")
                if base_url !="":
                    openai.base_url = base_url
                elif api_keys.get('base_url')!="":  
                    openai.base_url = api_keys.get('base_url')
                else:
                    openai.base_url = os.environ.get("OPENAI_API_BASE")
                if openai.api_key =="":
                    return ("请输入API_KEY",)
                
                # 读取prompt.json文件
                with open(self.prompt_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                tool_list=[]
                if is_tools_in_sys_prompt=="enable":
                    if tools is not None:
                        tools_dis=json.loads(tools)
                        for tool_dis in tools_dis:
                            tool_list.append(tool_dis["function"])
                        system_prompt=system_prompt+"\n"+"你可以使用以下工具："
                else:
                    tool_list=[]

                for message in history:
                    if message['role'] == 'system':
                        message['content'] = system_prompt
                        if tool_list!=[]:
                            message['tools']=tool_list
                        else:
                            if 'tools' in message:
                                # 如果存在，移除 'tools' 键值对
                                message.pop('tools')
                
                if tools is not None:
                    print(tools)
                    tools=json.loads(tools)
                chat=Chat(history, model_name, temperature,max_length,tools)

                if file_content is not None:
                    user_prompt="文件中相关内容："+file_content+"\n"+"用户提问："+user_prompt+"\n"+"请根据文件内容回答用户问题。\n"+"如果无法从文件内容中找到答案，请回答“抱歉，我无法从文件内容中找到答案。”"
                
                if images is not None:
                    if imgbb_api_key=="" or imgbb_api_key is None:
                        imgbb_api_key=api_keys.get('imgbb_api')
                    i = 255. * images[0].cpu().numpy()
                    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))         
                    # 将图片保存到缓冲区
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")                   
                    # 将图片编码为base64
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    url = "https://api.imgbb.com/1/upload"
                    payload = {
    'key': imgbb_api_key,
    'image': img_str
}
                    # 向API发送POST请求
                    response = requests.post(url, data=payload)
                    # 检查请求是否成功
                    if response.status_code == 200:
                        # 解析响应以获取图片URL
                        result = response.json()
                        img_url=result['data']['url']
                    else:
                        return "Error: " + response.text
                    img_json=[
    {"type": "text", "text": user_prompt},
    {
        "type": "image_url",
        "image_url": {
        "url": img_url,
        },
    },
    ]
                    user_prompt=json.dumps(img_json,ensure_ascii=False,indent=4)

                response,history= chat.send(user_prompt)
                print(response)
                #修改prompt.json文件
                with open(self.prompt_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                history=str(history)
                return (response,history,llm_tools_json,)
            except Exception as ex:
                print(ex)
                return (str(ex),str(ex),llm_tools_json,)
    @classmethod
    def IS_CHANGED(s):
        # 返回当前时间的哈希值，确保每次都不同
        current_time = str(time.time())
        return hashlib.sha256(current_time.encode()).hexdigest()


def llm_chat(model,tokenizer,user_prompt,history,device,max_length,role="user"):
    history.append({"role": role, "content": user_prompt.strip()})
    text = tokenizer.apply_chat_template(
        history,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=max_length,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    history.append({"role":"assistant","content":response})
    return response,history



class LLM_local:
    def __init__(self):
        #生成一个hash值作为id
        self.id=hash(str(self))
        global instances
        instances.append(self)
        # 构建prompt.json的绝对路径
        self.prompt_path = os.path.join(current_dir_path,"temp", str(self.id)+'.json')
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": "你是一个强大的人工智能助手。"}], f, indent=4, ensure_ascii=False)
        self.tool_data={"id":self.id,"system_prompt":"","type":"local"}
        self.list=[]
        self.added_to_list = False
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你一个强大的人工智能助手。"
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": "你好",
                }),
                "model_type": (["GLM", "llama","Qwen"], {
                    "default": "GLM",
                }),
                "model_path": ("STRING", {
                    "default": None,
                }),
                "tokenizer_path": ("STRING", {
                    "default": None,
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "is_memory": (["enable", "disable"],{
                    "default":"enable"
                }),
                "is_tools_in_sys_prompt": (["enable", "disable"],{
                    "default":"disable"
                }),
                "is_locked": (["enable", "disable"],{
                    "default":"disable"
                }),
                "is_reload": (["enable", "disable"],{
                    "default":"disable"
                }),
                "main_brain": (["enable", "disable"],{
                    "default":"enable"
                }),
                "device": (["cuda","cuda-float16","cuda-int8","cuda-int4","cpu"], {
                    "default": "cuda" if torch.cuda.is_available() else "cpu",
                }),
                "max_length": ("INT", {
                    "default": 512,
                    "min": 256,
                    "step": 256
                })
            },
            "optional": {
                "tools": ("STRING", {
                    "forceInput": True
                }),
                "file_content": ("STRING", {
                    "forceInput": True
                })
            }
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("assistant_response","history","tool",)

    FUNCTION = "chatbot"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）"

    def chatbot(self, user_prompt, main_brain,system_prompt,model_type,temperature,model_path,max_length,tokenizer_path,is_reload,device,is_memory,is_tools_in_sys_prompt,is_locked,tools=None,file_content=None):
        self.list=[main_brain,system_prompt,model_type,temperature,model_path,max_length,tokenizer_path,is_reload,device,is_memory,is_tools_in_sys_prompt,is_locked,tools,file_content]
        self.tool_data["system_prompt"]=system_prompt
        global llm_tools_list,llm_tools
        if main_brain=="disable":
            if not self.added_to_list:
                llm_tools_list.append(self.tool_data)
                self.added_to_list = True
        llm_tools=[{
    "type": "function",
    "function": {
        "name": "another_llm",
        "description": "使用llm_tools可以调用其他的智能助手解决你的问题。请根据以下列表中的system_prompt选择你需要的智能助手："+json.dumps(llm_tools_list,ensure_ascii=False,indent=4),
        "parameters": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "智能助手的id"},
                "type": {"type": "string", "description": "智能助手的类型，目前支持api和local两种类型。"},
                "question": {"type": "string", "description": "问题描述，代表你想要解决的问题。"},
            },
            "required": ["id","type","question"]
        }
    }
}]
        llm_tools_json=json.dumps(llm_tools,ensure_ascii=False,indent=4)
        if user_prompt=="#清空":
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": system_prompt}], f, indent=4, ensure_ascii=False)
                            
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return ("已清空历史记录",str(history),llm_tools_json,)
        elif user_prompt is None or user_prompt.strip()=="empty":
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
            return ("",str(history),llm_tools_json,)
        else:
            try:
                # 读取prompt.json文件
                with open(self.prompt_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                if is_locked=="enable":
                    #返回对话历史中，最后一个content
                    return (history[-1]['content'],str(history),)
                if is_memory=="disable":
                    with open(self.prompt_path, 'w', encoding='utf-8') as f:
                        json.dump([{"role": "system","content": system_prompt}], f, indent=4, ensure_ascii=False)
                
                # 读取prompt.json文件
                with open(self.prompt_path, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                tools_list=[]
                if tools is not None:
                    tools_dis=json.loads(tools)
                    for tool_dis in tools_dis:
                        tools_list.append(tool_dis["function"])
                for message in history:
                    if message['role'] == 'system':
                        message['content'] = system_prompt
                        if tools_list!=[]:
                            if model_type=="GLM":
                                message['content']+="\n"+"你可以使用以下工具："
                                message['tools']=tools_list
                            elif model_type=="llama":
                                message['content']+="You can invoke the following tools by constructing a JSON object: " + json.dumps(tools_list, ensure_ascii=False) + "\n Tool usage instructions: You need to build a JSON object based on the names and parameters of these tools. For example, if you want to call a tool named 'tool_name' and need to pass parameters 'param1' and 'param2', you should construct a JSON object in the following format: {\"name\":\"tool_name\",\"parameters\":{\"param1\":\"value1\",\"param2\":\"value2\"}}\nWhen invoking tools, please construct a JSON object based on the names and parameters specified in the aforementioned tools. Avoid including any parameters not indicated in the tools, and ensure that you do not omit any required parameters explicitly mentioned by the tools. Additionally, refrain from outputting any content other than the JSON object when calling the tools."
                            elif model_type=="Qwen":
                                message['content']+="你可以通过构建一个JSON对象来调用以下工具：" + json.dumps(tools_list, ensure_ascii=False) + "\n工具使用说明：您需要根据这些工具的名称和参数构建一个JSON对象。例如，如果您想调用一个名为“tool_name”的工具，并且需要传递参数“param1”和“param2”，您应该按照以下格式构建一个JSON对象：{\"name\":\"tool_name\",\"parameters\":{\"param1\":\"value1\",\"param2\":\"value2\"}}\n在调用工具时，请根据上述工具中指定的名称和参数构建一个JSON对象。请避免包含工具中未指定的任何参数，并确保不要省略工具明确提到的任何必需参数。此外，在调用工具时，请不要输出除JSON对象之外的任何内容。"
                        else:
                            if 'tools' in message:
                                # 如果存在，移除 'tools' 键值对
                                message.pop('tools')
                
                if tools is not None:
                    print(tools)
                    tools=json.loads(tools)
                def is_valid_json(json_str):
                    try:
                        json.loads(json_str)
                        return True
                    except json.JSONDecodeError:
                        return False
                
                if file_content is not None:
                    user_prompt="文件中相关内容："+file_content+"\n"+"用户提问："+user_prompt+"\n"+"请根据文件内容回答用户问题。\n"+"如果无法从文件内容中找到答案，请回答“抱歉，我无法从文件内容中找到答案。”"
                global glm_tokenizer, glm_model, llama_tokenizer, llama_model,qwen_tokenizer, qwen_model
                if model_type=="GLM":
                    if glm_tokenizer=="":
                        glm_tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
                    if glm_model=="":
                        if device=="cuda":
                            glm_model = AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()
                        elif device=="cuda-float16":
                            glm_model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda()
                        elif device=="cuda-int8":
                            glm_model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().quantize(8).cuda()
                        elif device=="cuda-int4":
                            glm_model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().quantize(4).cuda()
                        else:
                            glm_model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float()
                        glm_model = glm_model.eval()
                    response, history= glm_model.chat(glm_tokenizer, user_prompt,history,temperature=temperature,max_length=max_length,role="user")
                    while type(response) == dict:
                        if response['name']=="interpreter":
                            result =interpreter(str(response['content']))
                            response, history = glm_model.chat(glm_tokenizer, result, history=history, role="observation")
                        else:
                            result = dispatch_tool(response['name'],response['parameters'])
                            print(result)
                            response, history = glm_model.chat(glm_tokenizer, result, history=history, role="observation")
                elif model_type=="llama":
                    llama_device = "cuda" if torch.cuda.is_available() else "cpu"
                    if llama_tokenizer=="":
                        llama_tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
                    if llama_model=="":
                        if device=="cuda":
                            llama_model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True,device_map="cuda")
                        elif device=="cpu":
                            llama_model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True).float()
                        else:
                            llama_model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True).half().cuda()
                        llama_model = llama_model.eval()
                    response, history = llm_chat(llama_model,llama_tokenizer,user_prompt,history,llama_device,max_length)
                    while is_valid_json(response):
                        response = json.loads(response)
                        result = dispatch_tool(response['name'],response['parameters'])
                        print(result)
                        response, history = llm_chat(qwen_model,qwen_tokenizer,user_prompt,history,qwen_device,max_length,role="observation")
                elif model_type=="Qwen":
                    qwen_device = "cuda" if torch.cuda.is_available() else "cpu"
                    if qwen_tokenizer=="":
                        qwen_tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, revision='master', trust_remote_code=True)
                    if qwen_model=="":
                        if device=="cuda":
                            qwen_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True, fp32=True,fp16=False,bf16=False).eval()
                        elif device=="cpu":
                            qwen_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cpu", trust_remote_code=True, fp32=True,fp16=False,bf16=False).eval()
                        else:
                            qwen_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", trust_remote_code=True, fp16=True,fp32=False,bf16=False).eval()
                        qwen_model.eval()
                    qwen_model.generation_config = GenerationConfig.from_pretrained(model_path, trust_remote_code=True)
                    response, history = qwen_model.chat(qwen_tokenizer, user_prompt, history=history)
                    while is_valid_json(response):
                        print(response)
                        response = json.loads(response)
                        result = dispatch_tool(response['name'],response['parameters'])
                        print(result)
                        response, history = qwen_model.chat(qwen_tokenizer, user_prompt, history=history)
                print(response)
                #修改prompt.json文件
                with open(self.prompt_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                history=str(history)
                if is_reload=="enable":
                    del glm_model
                    del glm_tokenizer
                    del llama_model
                    del llama_tokenizer
                    del qwen_model
                    del qwen_tokenizer
                    torch.cuda.empty_cache()
                    gc.collect() 
                    glm_tokenizer=""
                    glm_model=""
                    llama_tokenizer=""
                    llama_model=""
                    qwen_tokenizer=""
                    qwen_model=""
                return (response,history,llm_tools_json,)
            except Exception as ex:
                print(ex)
                return (str(ex),str(ex),llm_tools_json,)
    @classmethod
    def IS_CHANGED(s):
        # 返回当前时间的哈希值，确保每次都不同
        current_time = str(time.time())
        return hashlib.sha256(current_time.encode()).hexdigest()







NODE_CLASS_MAPPINGS = {
    "LLM": LLM,
    "LLM_local": LLM_local,
    "load_file":load_file,
    "load_persona":load_persona,
    "classify_persona":classify_persona,
    "classify_function":classify_function,
    "tool_combine":tool_combine,
    "tool_combine_plus":tool_combine_plus,
    "time_tool": time_tool,
    "weather_tool":weather_tool,
    "google_tool":google_tool,
    "check_web_tool":check_web_tool,
    "file_combine":file_combine,
    "file_combine_plus":file_combine_plus,
    "start_dialog":start_dialog,
    "end_dialog":end_dialog,
    "interpreter_tool":interpreter_tool,
    "ebd_tool":ebd_tool,
    "custom_persona":custom_persona,
    "start_workflow":start_workflow,
    "end_workflow":end_workflow,
    "new_interpreter_tool":new_interpreter_tool,
    "CLIPTextEncode_party":CLIPTextEncode_party,
    "KSampler_party":KSampler_party,
    "VAEDecode_party":VAEDecode_party,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "LLM": "大语言模型api（LLM_api）",
    "LLM_local":"本地大语言模型（LLM_local）",
    "load_file": "加载文件（load_file）",
    "load_persona": "加载人格面具（load_persona）",
    "classify_persona": "分类器面具（classify_persona）",
    "classify_function": "分类器函数（classify_function）",
    "tool_combine":"工具组合（tool_combine）",
    "tool_combine_plus":"超大工具组合（tool_combine_plus）",
    "time_tool": "时间工具（time_tool）",
    "weather_tool":"天气工具（weather_tool）",
    "google_tool":"谷歌搜索工具（google_tool）",
    "check_web_tool":"检视网页工具(check_web_tool)",
    "file_combine":"文件组合（file_combine）",
    "file_combine_plus":"超大文件组合（file_combine_plus）",
    "start_dialog":"开始对话（start_dialog）",
    "end_dialog":"结束对话（end_dialog）",
    "interpreter_tool":"解释器工具（interpreter_tool）",
    "ebd_tool":"词嵌入模型工具（embeddings_tool）",
    "custom_persona":"自定义面具（custom_persona）",
    "start_workflow":"开始工作流（start_workflow）",
    "end_workflow":"结束工作流（end_workflow）",
    "new_interpreter_tool":"万能解释器工具（omnipotent_interpreter_tool）",
    "CLIPTextEncode_party":"CLIP文本编码器（CLIPTextEncode_party）",
    "KSampler_party":"KSampler采样器（KSampler_party）",
    "VAEDecode_party":"VAEDecode解码器（VAEDecode_party）",
}

if __name__ == '__main__':
    llm=LLM()
    res=llm.chatbot("你好", "你是一个强大的人工智能助手。", "gpt-3.5-turbo",0.7,tools=time_tool().time("Asia/Shanghai"))
