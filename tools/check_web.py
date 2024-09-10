import json
import os

import openai
import requests
import torch
from bs4 import BeautifulSoup
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

from ..config import config_path, current_dir_path, load_api_keys

bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""
is_jina = True


def check_web(url, keyword=None):
    """
    获取网站页面上与关键词相关的文字信息。

    :param url: 网站的URL。
    :param keyword: 搜索的关键词。
    :return: 与关键词相关的文本内容。
    """
    try:
        global bge_embeddings, c_size, c_overlap

        jina = "https://r.jina.ai/"
        global is_jina
        if is_jina:
            url = jina + url

            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 确保请求成功

            # 设置响应内容的编码，确保文本不会出现编码问题
            response.encoding = response.apparent_encoding
            res = response.text
        else:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 确保请求成功

            # 设置响应内容的编码，确保文本不会出现编码问题
            response.encoding = response.apparent_encoding
            # 假设response.text包含你的HTML内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 移除所有script和style元素
            for script in soup(["script", "style"]):
                script.extract()

            # 获取纯文本内容
            res = soup.get_text()

        if keyword == None or keyword == "":
            combined_content = str(res)
            return "该网页的相关信息为：" + str(combined_content)
        elif bge_embeddings == "":
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small", api_key=openai.api_key, base_url=openai.base_url
            )
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=c_size,
                chunk_overlap=c_overlap,
            )
            chunks = text_splitter.split_text(str(response.text))
            url_base = FAISS.from_texts(chunks, embeddings)
            docs = url_base.similarity_search(keyword, k=5)
            combined_content = "".join(doc.page_content + "\n" for doc in docs)
            return "该网页的相关信息为：" + str(combined_content)
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=c_size,
                chunk_overlap=c_overlap,
            )
            chunks = text_splitter.split_text(str(response.text))
            url_base = FAISS.from_texts(chunks, bge_embeddings)
            docs = url_base.similarity_search(keyword, k=5)
            combined_content = "".join(doc.page_content + "\n" for doc in docs)
            return "该网页的相关信息为：" + str(combined_content)
    except requests.RequestException as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


class check_web_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
            },
            "optional": {
                "web_url": ("STRING", {}),
                "embedding_path": ("STRING", {"default": ""}),
                "with_jina": ("BOOLEAN", {"default": True}),
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
                "ebd_model": ("EBD_MODEL", {"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "read_web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def read_web(
        self,
        chunk_size,
        chunk_overlap,
        device,
        with_jina=True,
        is_enable=True,
        web_url="",
        embedding_path="",
        api_key="sk-XXXXX",
        base_url="https://api.openai.com/v1/",
        ebd_model=None,
    ):
        if is_enable == False:
            return (None,)
        global files_load, bge_embeddings, c_size, c_overlap, knowledge_base, is_jina
        is_jina = with_jina
        c_size = chunk_size
        c_overlap = chunk_overlap
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        if ebd_model is None:
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
            if bge_embeddings == "" and embedding_path is not None and embedding_path != "":
                bge_embeddings = HuggingFaceBgeEmbeddings(
                    model_name=embedding_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
                )
        else:
            bge_embeddings = ebd_model
        if (embedding_path is None or embedding_path == "") and ebd_model is None:
            os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
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

        if web_url is not None and web_url != "":
            output = [
                {
                    "type": "function",
                    "function": {
                        "name": "check_web",
                        "description": "通过关键词搜索一个给定url的网页上的信息。",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "要被搜索的网页的URL", "default": web_url},
                                "keyword": {
                                    "type": "string",
                                    "description": "需要搜索的关键词，如果没有关键词，则搜索网页上的所有内容",
                                },
                            },
                            "required": ["url"],
                        },
                    },
                }
            ]

        else:
            output = [
                {
                    "type": "function",
                    "function": {
                        "name": "check_web",
                        "description": "通过关键词搜索一个给定url的网页上的信息。",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "要被搜索的网页的URL"},
                                "keyword": {
                                    "type": "string",
                                    "description": "需要搜索的关键词，如果没有关键词，则搜索网页上的所有内容",
                                },
                            },
                            "required": ["url", "keyword"],
                        },
                    },
                }
            ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)
