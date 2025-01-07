import json

import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    def __init__(self):
        self.file_content = ""
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default":""}),
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
                "ebd_model": ("EBD_MODEL", {"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/知识库（Knowbase）"

    def file(self, model_path, k, chunk_size, chunk_overlap, device, file_content="", is_enable="enable", base_path="",ebd_model=None):
        if is_enable == "disable":
            return (None,)
        global files_load, bge_embeddings, c_size, c_overlap, knowledge_base, k_setting
        k_setting = k
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        c_size = chunk_size
        c_overlap = chunk_overlap
        if bge_embeddings == "":
            if ebd_model is None:
                model_kwargs = {"device": device}
                encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
                bge_embeddings = HuggingFaceBgeEmbeddings(
                    model_name=model_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
                )
            else:
                bge_embeddings = ebd_model
        if base_path != "":
            knowledge_base = FAISS.load_local(base_path, bge_embeddings, allow_dangerous_deserialization=True)
        else:
            self.file_content = file_content
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=c_size,
                chunk_overlap=c_overlap,
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
class load_ebd:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": ""}),
                "is_enable": ("BOOLEAN", {"default": True}),
                "device": (
                    ["auto", "cuda", "mps", "cpu"],
                    {"default": ("auto")},
                ),
            },
        }

    RETURN_TYPES = ("EBD_MODEL",)
    RETURN_NAMES = ("ebd_model",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/模型加载器（model loader）"

    def file(self, model_path, device, is_enable=True):
        if is_enable == False:
            return (None,)
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        model_kwargs = {"device": device}
        encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
        bge_embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        )
        return (bge_embeddings,)

class embeddings_function:
    def __init__(self):
        self.embeddings = ""
        self.embeddings_path = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": None}),
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
                "ebd_model": ("EBD_MODEL", {"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ebd_response",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def file(self, model_path, question, k, chunk_size, chunk_overlap, device, file_content="", is_enable=True, base_path="",ebd_model=None):
        if is_enable == False:
            return (None,)
        if ebd_model is None:
            if device == "auto":
                device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

            if self.embeddings_path != model_path:
                model_kwargs = {"device": device}
                encode_kwargs = {"normalize_embeddings": True}  # 设置为 True 以计算余弦相似度
                self.bge_embeddings = HuggingFaceBgeEmbeddings(
                    model_name=model_path, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
                )
                self.embeddings_path = model_path
        else:
            self.bge_embeddings = ebd_model
        if base_path != "":
            base = FAISS.load_local(base_path, self.bge_embeddings, allow_dangerous_deserialization=True)
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
            base = FAISS.from_texts(chunks, self.bge_embeddings)
        docs = base.similarity_search(question, k=k)
        combined_content = "".join(doc.page_content + "\n\n" for doc in docs)
        output = combined_content
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

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

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
        base = FAISS.from_texts(chunks, self.bge_embeddings)
        # 保存 FAISS 数据库到本地 save_path
        base.save_local(save_path)
        return ()
