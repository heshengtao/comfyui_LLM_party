import json

import requests
import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

ebd_model = ""
bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""


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
        url = jina + url

        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 确保请求成功

        # 设置响应内容的编码，确保文本不会出现编码问题
        response.encoding = response.apparent_encoding

        if keyword == None or keyword == "" or bge_embeddings == "":
            combined_content = str(response.text)
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
                "embedding_path": ("STRING", {"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "read_web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def read_web(self, chunk_size, chunk_overlap, device, is_enable=True, web_url=None, embedding_path=None):
        if is_enable == False:
            return (None,)
        global ebd_model, files_load, bge_embeddings, c_size, c_overlap, knowledge_base
        c_size = chunk_size
        c_overlap = chunk_overlap
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        if ebd_model == "":
            model_kwargs = {"device": device}
            encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
        if bge_embeddings == "" and embedding_path is not None and embedding_path != "":
            bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=embedding_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )

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
