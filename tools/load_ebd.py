import json
import os
import openai
from openai import OpenAI
import requests
import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..config import config_path, current_dir_path, load_api_keys

bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""
k_setting = 5


def data_base(question):
    global knowledge_base, k_setting
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
                "k": ("INT", {"default": 5}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "base_path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def file(self, path, k, chunk_size, chunk_overlap, device, file_content="", is_enable="enable", base_path=""):
        if is_enable == "disable":
            return (None,)
        global files_load, bge_embeddings, c_size, c_overlap, knowledge_base, k_setting
        k_setting = k
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        c_size = chunk_size
        c_overlap = chunk_overlap
        files_load = file_content
        if bge_embeddings == "":
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
        if base_path != "":
            knowledge_base = FAISS.load_local(base_path, bge_embeddings, allow_dangerous_deserialization=True)
        elif knowledge_base == "":
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
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
                "k": ("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {
                "file_content": ("STRING", {"forceInput": True}),
                "base_path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ebd_response",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, path, question, k, chunk_size, chunk_overlap, device, file_content="", is_enable=True, base_path=""):
        if is_enable == False:
            return (None,)
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        if self.embeddings_path != path:
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            self.bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            self.embeddings_path = path
        if base_path != "":
            base = FAISS.load_local(base_path, self.bge_embeddings, allow_dangerous_deserialization=True)
        else:
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


class save_ebd_database:
    def __init__(self):
        self.embeddings = ""
        self.embeddings_path = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": ""}),
                "save_path": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {},
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "file"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/函数（function）"

    def file(self, model_path, save_path, file_content, chunk_size, chunk_overlap, device, is_enable=True):
        if is_enable == False:
            return (None,)
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        if self.embeddings_path != model_path:
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            self.bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=model_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            self.embeddings_path = model_path
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks = text_splitter.split_text(file_content)
        base = FAISS.from_texts(chunks, self.bge_embeddings)
        # 保存 FAISS 数据库到本地 save_path
        base.save_local(save_path)
        return ()

class load_openai_ebd:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_name":("STRING", {"default": "text-embedding-3-small"}),
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ebd_response",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/加载器（loader）"

    def file(self, model_name, question, k, chunk_size, chunk_overlap, file_content="", is_enable=True, base_path="", base_url=None, api_key=None):
        if is_enable == False:
            return (None,)
        
        api_keys = load_api_keys(config_path)
        if api_key != "":
            openai.api_key = api_key
        elif api_keys.get("openai_api_key") != "":
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        if base_url != "":
            # 如果以/结尾
            if base_url[-1] == "/":
                openai.base_url = base_url
            else:
                openai.base_url = base_url + "/"
        elif api_keys.get("base_url") != "":
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")
        if openai.api_key == "":
            return ("请输入API_KEY",)
        client = OpenAI(api_key=openai.api_key, base_url=openai.base_url)

        # 将文件内容按段落分割
        paragraphs = file_content.split('\n')
        
        # 根据chunk_size和chunk_overlap处理段落
        chunks = []
        for i in range(0, len(paragraphs), chunk_size - chunk_overlap):
            chunk = "\n".join(paragraphs[i:i + chunk_size])
            chunks.append(chunk)
        
        paragraph_embeddings = [client.embeddings.create(model=model_name, input=[chunk]).data[0].embedding for chunk in chunks]
        
        # 获取问题的嵌入表示
        question_embedding = client.embeddings.create(model=model_name, input=[question]).data[0].embedding
        
        # 计算每个段落与问题的相似度
        similarities = [torch.cosine_similarity(torch.tensor(question_embedding), torch.tensor(pe), dim=0).item() for pe in paragraph_embeddings]
        
        # 获取相似度最高的 k 个段落
        most_relevant_paragraphs = sorted(zip(similarities, chunks), reverse=True)[:k]
        combined_content = "\n".join([p for _, p in most_relevant_paragraphs])
        
        output = "文件中的相关信息如下：\n" + combined_content
        return (output,)