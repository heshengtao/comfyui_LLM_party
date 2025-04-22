import configparser
import json
import locale
import os
import pickle

import openai
import requests
import torch
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings,AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")


def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


api_base = ""
api_k = 5


def openai_data_base(question):
    global api_base, api_k
    docs = api_base.similarity_search(question, k=api_k)
    combined_content = "".join(doc.page_content + "\n\n" for doc in docs)
    output = "文件中的相关信息如下：\n" + combined_content
    return output


class load_openai_ebd:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "text-embedding-3-small"}),
                "question": ("STRING", {"default": "question"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "k": ("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "base_path": ("STRING", {"default": ""}),
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ebd_response",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def file(
        self,
        model_name,
        question,
        k,
        chunk_size,
        chunk_overlap,
        file_content="",
        is_enable=True,
        base_path="",
        base_url=None,
        api_key=None,
        is_ollama=False,
    ):
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        if not is_enable:
            return (None,)

        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")

        embeddings = OpenAIEmbeddings(model=model_name, api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            embeddings = AzureOpenAIEmbeddings(
                model=model_name,
                api_key=openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        if is_ollama:
            if base_url:
                openai.base_url = base_url.rstrip("/") + "/"
            else:
                openai.base_url = "http://127.0.0.1:11434/"
            embeddings = OllamaEmbeddings(model=model_name, base_url=openai.base_url)
        if not base_path:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            # 判断file_content是否可以被json load
            try:
                files_load = json.loads(file_content)
            except json.JSONDecodeError:
                files_load = file_content
            
            if isinstance(files_load, str):
                chunks = text_splitter.split_text(files_load)
            elif isinstance(files_load, list):
                chunks = []
                for file in files_load:
                    content= file["file_content"]
                    chunks_list = text_splitter.split_text(content)
                    i = 1
                    for chunk in chunks_list:
                        new_chunk = {"source": file["source"],"paragraph_index":str(i) , "file_content": chunk}
                        chunks.append(json.dumps(new_chunk, ensure_ascii=False))
                        i += 1
            # 使用FAISS存储嵌入表示
            base = FAISS.from_texts(chunks, embeddings)
        else:
            # 加载base_path的数据库到FAISS
            base = FAISS.load_local(base_path, embeddings, allow_dangerous_deserialization=True)

        docs = base.similarity_search(question, k=k)
        combined_content = "".join(doc.page_content + "\n\n" for doc in docs)
        output = combined_content
        return (output,)


class openai_ebd_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "text-embedding-3-small"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "k": ("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "base_path": ("STRING", {"default": ""}),
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(
        self,
        model_name,
        k,
        chunk_size,
        chunk_overlap,
        file_content="",
        is_enable=True,
        base_path="",
        base_url=None,
        api_key=None,
        is_ollama=False,
    ):
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        if not is_enable:
            return (None,)

        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            api_keys = load_api_keys(config_path)
            openai.api_key = api_keys.get("openai_api_key")
            openai.base_url = api_keys.get("base_url")

        embeddings = OpenAIEmbeddings(model=model_name, api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            embeddings = AzureOpenAIEmbeddings(
                model=model_name,
                api_key=openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        if is_ollama:
            if base_url:
                openai.base_url = base_url.rstrip("/") + "/"
            else:
                openai.base_url = "http://127.0.0.1:11434/"
            embeddings = OllamaEmbeddings(model=model_name, base_url=openai.base_url)
        if not base_path:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            # 判断file_content是否可以被json load
            try:
                files_load = json.loads(file_content)
            except json.JSONDecodeError:
                files_load = file_content
            
            if isinstance(files_load, str):
                chunks = text_splitter.split_text(files_load)
            elif isinstance(files_load, list):
                chunks = []
                for file in files_load:
                    content= file["file_content"]
                    chunks_list = text_splitter.split_text(content)
                    i = 1
                    for chunk in chunks_list:
                        new_chunk = {"source": file["source"],"paragraph_index":str(i) , "file_content": chunk}
                        chunks.append(json.dumps(new_chunk, ensure_ascii=False))
                        i += 1

            # 使用FAISS存储嵌入表示
            base = FAISS.from_texts(chunks, embeddings)
        else:
            # 加载base_path的数据库到FAISS
            base = FAISS.load_local(base_path, embeddings, allow_dangerous_deserialization=True)
        global api_base, api_k
        api_base = base
        api_k = k
        output = [
            {
                "type": "function",
                "function": {
                    "name": "openai_data_base",
                    "description": "在知识库里查询与用户提问相关的信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "要查询的关键词"},
                        },
                        "required": ["question"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class save_openai_ebd:
    def __init__(self):
        self.embeddings = ""
        self.embeddings_path = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name": ("STRING", {"default": "text-embedding-3-small"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
                "save_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
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

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "file"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def file(
        self,
        model_name,
        chunk_size,
        chunk_overlap,
        file_content="",
        is_enable=True,
        save_path="",
        base_url=None,
        api_key=None,
        is_ollama=False,
    ):
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        if not is_enable:
            return (None,)

        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)

        embeddings = OpenAIEmbeddings(model=model_name, api_key=openai.api_key, base_url=openai.base_url)
        if "openai.azure.com" in openai.base_url:
            # 获取API版本
            api_version = openai.base_url.split("=")[-1].split("/")[0]
            # 获取azure_endpoint
            azure_endpoint = "https://"+openai.base_url.split("//")[1].split("/")[0]
            embeddings = AzureOpenAIEmbeddings(
                model=model_name,
                api_key=openai.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
            )
        if is_ollama:
            if base_url:
                openai.base_url = base_url.rstrip("/") + "/"
            else:
                openai.base_url = "http://127.0.0.1:11434/"
            embeddings = OllamaEmbeddings(model=model_name, base_url=openai.base_url)
        # 将文件内容按段落分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        # 判断file_content是否可以被json load
        try:
            files_load = json.loads(file_content)
        except json.JSONDecodeError:
            files_load = file_content
        
        if isinstance(files_load, str):
            chunks = text_splitter.split_text(files_load)
        elif isinstance(files_load, list):
            chunks = []
            for file in files_load:
                content= file["file_content"]
                chunks_list = text_splitter.split_text(content)
                i = 1
                for chunk in chunks_list:
                    new_chunk = {"source": file["source"],"paragraph_index":str(i) , "file_content": chunk}
                    chunks.append(json.dumps(new_chunk, ensure_ascii=False))
                    i += 1

        # 使用FAISS存储嵌入表示
        base = FAISS.from_texts(chunks, embeddings)
        # 保存 FAISS 数据库到本地 save_path
        base.save_local(save_path)

        return ()


_TOOL_HOOKS = ["openai_data_base"]
NODE_CLASS_MAPPINGS = {
    "load_openai_ebd": load_openai_ebd,
    "save_openai_ebd": save_openai_ebd,
    "openai_ebd_tool": openai_ebd_tool,
}
# 获取系统语言
lang = locale.getlocale()[0]
if 'Chinese' in lang:
   lang = 'zh_CN'
else:
   lang = 'en_US'
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_openai_ebd": "☁️openai词向量搜索",
        "save_openai_ebd": "☁️保存openai词嵌入数据库",
        "openai_ebd_tool": "☁️openai词嵌入数据库工具",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "load_openai_ebd": "☁️OpenAI Word Vector Search",
        "save_openai_ebd": "☁️Save OpenAI Embeddings database",
        "openai_ebd_tool": "☁️OpenAI Embeddings database Tool",
    }
