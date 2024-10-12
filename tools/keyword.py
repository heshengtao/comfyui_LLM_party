import json
from collections import Counter

import requests
import torch
from langchain_text_splitters import RecursiveCharacterTextSplitter

ebd_model = ""
bge_embeddings = ""
files_load = ""
c_size = 200
c_overlap = 50
knowledge_base = ""
k_setting = 5


def search_keyword(question):
    global knowledge_base, k_setting
    keyword_counts = [chunk.count(question) for chunk in knowledge_base]
    chunk_counter = Counter(dict(zip(knowledge_base, keyword_counts)))
    top_chunks = chunk_counter.most_common(k_setting)
    top_chunks_text = [chunk[0] for chunk in top_chunks]
    text = "\n".join(top_chunks_text)

    return "文件中的相关信息如下：\n" + text


class keyword_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": (["enable", "disable"], {"default": "enable"}),
                "file_content": ("STRING", {"forceInput": True}),
                "k": ("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, file_content, k, chunk_size, chunk_overlap, is_enable="enable"):
        if is_enable == "disable":
            return (None,)
        global files_load, c_size, c_overlap, knowledge_base, k_setting
        k_setting = k
        c_size = chunk_size
        c_overlap = chunk_overlap
        files_load = file_content
        if knowledge_base == "":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=c_size,
                chunk_overlap=c_overlap,
            )
            chunks = text_splitter.split_text(files_load)
            knowledge_base = chunks
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_keyword",
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


class load_keyword:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "question": ("STRING", {"default": "question"}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "file_content": ("STRING", {"forceInput": True}),
                "k": ("INT", {"default": 5}),
                "chunk_size": ("INT", {"default": 200}),
                "chunk_overlap": ("INT", {"default": 50}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("relative_info",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def file(self, question, file_content, k, chunk_size, chunk_overlap, is_enable=True):
        if is_enable == False:
            return (None,)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        chunks = text_splitter.split_text(file_content)
        keyword_counts = [chunk.count(question) for chunk in chunks]
        chunk_counter = Counter(dict(zip(chunks, keyword_counts)))
        top_chunks = chunk_counter.most_common(k)
        top_chunks_text = [chunk[0] for chunk in top_chunks]
        text = "\n".join(top_chunks_text)
        output = "文件中的相关信息如下：\n" + text
        return (output,)
