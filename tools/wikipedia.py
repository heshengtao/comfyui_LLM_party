import json

import torch
import wikipedia
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

ebd_model = ""
bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""


def get_wikipedia(query):
    global bge_embeddings, c_size, c_overlap
    if bge_embeddings == "":
        # 设置语言
        wikipedia.set_lang("zh")
        # 获取特定页面的内容
        py_page = wikipedia.page(query)
        res = py_page.content[:1000]
        return "维基百科上的相关信息为：\n" + res
    else:
        # 设置语言
        wikipedia.set_lang("zh")
        # 获取特定页面的内容
        py_page = wikipedia.page(query)
        res = py_page.content
        # 创建一个文本分割器，将文本分割成多个段落
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=c_size,
            chunk_overlap=c_overlap,
        )
        # 将文本分割成多个段落
        documents = text_splitter.split_text(res)
        # 创建一个向量存储
        vectorstore = FAISS.from_documents(documents, bge_embeddings)
        # 搜索与查询最相关的段落
        query_text = query
        query_embedding = bge_embeddings.embed_query(query_text)
        similar_documents = vectorstore.similarity_search(query_embedding, k=5)
        # 合并段落
        merged_text = "\n".join([document.page_content for document in similar_documents])
        # 返回合并后的文本
        return "维基百科上的相关信息为：\n" + merged_text


class wikipedia_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "query": ("STRING", {"default": "query"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
            },
            "optional": {
                "embedding_path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "wikipedia"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def wikipedia(self, query, embedding_path, chunk_size, chunk_overlap, device, is_enable="enable"):
        if is_enable == "disable":
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

        output = [
            {
                "type": "function",
                "function": {
                    "name": "get_wikipedia",
                    "description": "用于查询维基百科上的相关内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "需要查询的关键词，例如：python",
                                "default": str(query),
                            }
                        },
                        "required": ["query"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class load_wikipedia:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "query": ("STRING", {"default": "query"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_content",)

    FUNCTION = "wikipedia"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def wikipedia(self, query, is_enable=True):
        if is_enable == False:
            return (None,)
        # 设置语言
        wikipedia.set_lang("zh")
        # 获取特定页面的内容
        py_page = wikipedia.page(query)
        out = py_page.content
        return (out,)
