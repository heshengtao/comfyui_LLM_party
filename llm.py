import hashlib
import importlib
import json
import os
import sys
import time
import traceback
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import openai
from .config import config_path,current_dir_path,load_api_keys,bge_embeddings
from .tools.load_file import load_file
from .tools.tool_combine import tool_combine,tool_combine_plus
from .tools.get_time import get_time,time_tool
from .tools.get_weather import get_weather,weather_tool
from .tools.search_web import search_web,google_tool
from .tools.check_web import check_web,check_web_tool
from .tools.file_combine import file_combine,file_combine_plus
from .tools.dialog import start_dialog,end_dialog
from .tools.interpreter import interpreter,interpreter_tool


_TOOL_HOOKS=[
    "get_time",
    "get_weather",
    "search_web",
    "check_web",
    "interpreter",
]

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
    def __init__(self, history, model_name, temperature,tools=None) -> None:
        self.messages = history
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools

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
                    tools=self.tools
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
                    tools=self.tools
                    )
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
                        tools=self.tools
                    )
            else:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages,
                    temperature=self.temperature
                )
            print(response)
            response_content = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_content})
        except Exception as ex:
            response_content = "这个话题聊太久了，我想聊点别的了：" + str(ex)
        return response_content, self.messages



class LLM:
    def __init__(self):
        #生成一个hash值作为id
        self.id=hash(str(self))
        # 构建prompt.json的绝对路径
        self.prompt_path = os.path.join(current_dir_path,"temp", str(self.id)+'.json')
        # 如果文件不存在，创建prompt.json文件，存在就覆盖文件
        if not os.path.exists(self.prompt_path):
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": "你是一个强大的人工智能助手。"}], f, indent=4, ensure_ascii=False)


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
                    "max": 2.0,
                    "step": 0.1
                }),
                "is_memory": (["enable", "disable"],{
                    "default":"enable"
                }),
                "is_tools_in_sys_prompt": (["enable", "disable"],{
                    "default":"disable"
                }),
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
            }
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("assistant_response","history",)

    FUNCTION = "chatbot"

    #OUTPUT_NODE = False

    CATEGORY = "llm"

    def chatbot(self, user_prompt, system_prompt,model_name,temperature,is_memory,is_tools_in_sys_prompt,tools=None,file_content=None,api_key=None,base_url=None):
        if user_prompt=="#清空":
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                json.dump([{"role": "system","content": system_prompt}], f, indent=4, ensure_ascii=False)
            return ("已清空历史记录",)
        else:
            try:
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
                            message['tools']=None
                
                if tools is not None:
                    print(tools)
                    tools=json.loads(tools)
                chat=Chat(history,model_name,temperature,tools)
                
                if file_content is not None:
                    text_splitter0 = RecursiveCharacterTextSplitter(
                        chunk_size = 200,
                        chunk_overlap = 50,
                        ) 
                    chunks0 = text_splitter0.split_text(file_content)
                    knowledge_base0 = FAISS.from_texts(chunks0, bge_embeddings)
                    docs = knowledge_base0.similarity_search(user_prompt, k=5)
                    combined_content = ''.join(doc.page_content + "\n" for doc in docs)
                    user_prompt="文件中相关内容："+combined_content+"\n"+"用户提问："+user_prompt+"\n"+"请根据文件内容回答用户问题。\n"+"如果无法从文件内容中找到答案，请回答“抱歉，我无法从文件内容中找到答案。”"
                response,history= chat.send(user_prompt)
                print(response)
                #修改prompt.json文件
                with open(self.prompt_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=4, ensure_ascii=False)
                history=str(history)
                return (response,history,)
            except Exception as ex:
                print(ex)
                return (str(ex),str(ex),)
    @classmethod
    def IS_CHANGED(s):
        # 返回当前时间的哈希值，确保每次都不同
        current_time = str(time.time())
        return hashlib.sha256(current_time.encode()).hexdigest()


NODE_CLASS_MAPPINGS = {
    "LLM": LLM,
    "load_file":load_file,
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
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "LLM": "大语言模型（LLM）",
    "load_file": "从comfyui_LLM_party/file加载文件（load_file from comfyui_LLM_party/file）",
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
}

if __name__ == '__main__':
    llm=LLM()
    res=llm.chatbot("你好", "你是一个强大的人工智能助手。", "gpt-3.5-turbo",0.7,tools=time_tool().time("Asia/Shanghai"))
