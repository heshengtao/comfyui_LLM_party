import json
import locale

import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_list={}
def data_base_advance(question,file_name, k=5):
    global file_list
    k=int(k)
    knowledge_base= file_list[file_name]
    docs = knowledge_base.similarity_search(question, k=k)
    combined_content = "".join(doc.page_content + "\n" for doc in docs)
    return "文件中的相关信息如下：\n" + combined_content

class advance_ebd_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
                "is_enable": (["enable", "disable"], {"default": "enable"}),
                "k": ("INT", {"default": 5}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
                "file_name": ("STRING", {"default":""}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "base_path": ("STRING", {"default": ""}),
                "ebd_model": ("EBD_MODEL", {"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, path, k, chunk_size, chunk_overlap, device,file_name, file_content="", is_enable="enable", base_path="",ebd_model=None):
        if is_enable == "disable":
            return (None,)
        knowledge_base=""
        global  file_list
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        if ebd_model is None:
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
        else:
            bge_embeddings = ebd_model
        if base_path != "":
            knowledge_base = FAISS.load_local(base_path, bge_embeddings, allow_dangerous_deserialization=True)
        else:
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
            knowledge_base = FAISS.from_texts(chunks, bge_embeddings)
        file_list[file_name] = knowledge_base
        output = [
            {
                "type": "function",
                "function": {
                    "name": "data_base_advance",
                    "description": "查询用户上传的文件中与用户提问相关的信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "要查询的关键词"},
                            "file_name": {"type": "string", "description": f"要查询的知识库名，只能从{file_list.keys()}中选择。"},
                            "k": {"type": "string", "description": f"返回的段落数量，默认为{k}。"},
                        },
                        "required": ["question", "file_name", "k"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
_TOOL_HOOKS = ["data_base_advance"]
NODE_CLASS_MAPPINGS = {"advance_ebd_tool": advance_ebd_tool}
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
    NODE_DISPLAY_NAME_MAPPINGS = {"advance_ebd_tool": "💻高级词嵌入工具"}
else:
    NODE_DISPLAY_NAME_MAPPINGS = {"advance_ebd_tool": "💻Advanced Embedding Tool"}