import json

import requests
import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""
k_setting=5


def data_base(question):
    global knowledge_base,k_setting
    docs = knowledge_base.similarity_search(question, k=k_setting)
    combined_content = "".join(doc.page_content + "\n" for doc in docs)
    return "文件中的相关信息如下：\n" + combined_content


class ebd_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": None}),
                "is_enable": (["enable", "disable"], {"default": "enable"}),
                "file_content": ("STRING", {"forceInput": True}),
                "k": ("INT", {"default": 5}),
                "device": (
                    ["auto","cuda", "mps", "cpu"],
                    {
                        "default": (
                            "auto"
                        )
                    },
                ),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def file(self, path, file_content,k, chunk_size, chunk_overlap, device, is_enable="enable"):
        if is_enable == "disable":
            return (None,)
        global  files_load, bge_embeddings, c_size, c_overlap, knowledge_base,k_setting
        k_setting = k
        if device == "auto":
            device ="cuda"if torch.cuda.is_available()else ("mps" if torch.backends.mps.is_available() else "cpu")
        c_size = chunk_size
        c_overlap = chunk_overlap
        files_load = file_content
        if bge_embeddings == "":
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
        if knowledge_base == "":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=c_size,
                chunk_overlap=c_overlap,
            )
            chunks = text_splitter.split_text(files_load)
            knowledge_base = FAISS.from_texts(chunks, bge_embeddings)
        output = [
            {
                "type": "function",
                "function": {
                    "name": "data_base",
                    "description": "查询用户上传的文件中与用户提问相关的信息。",
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


class load_embeddings:
    def __init__(self):
        self.embeddings = ""
        self.embeddings_path = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"default": None}),
                "question": ("STRING", {"default": "question"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "device": (
                    ["auto","cuda", "mps", "cpu"],
                    {
                        "default": (
                            "auto"
                        )
                    },
                ),
                "k":("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ebd_response",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, path, question, file_content,k, chunk_size, chunk_overlap, device, is_enable=True):
        if is_enable == False:
            return (None,)
        if device == "auto":
            device ="cuda"if torch.cuda.is_available()else ("mps" if torch.backends.mps.is_available() else "cpu")

        if self.embeddings_path != path:
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            self.bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            self.embeddings_path = path
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks = text_splitter.split_text(file_content)
        base = FAISS.from_texts(chunks, self.bge_embeddings)
        docs = base.similarity_search(question, k=k)
        combined_content = "".join(doc.page_content + "\n\n" for doc in docs)
        output = "文件中的相关信息如下：\n" + combined_content
        return (output,)
