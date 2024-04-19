import json
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
ebd_model=""
bge_embeddings=""
files_load=""
def data_base(question):
    global bge_embeddings,files_load    
    text_splitter0 = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
        ) 
    chunks0 = text_splitter0.split_text(files_load)

    knowledge_base0 = FAISS.from_texts(chunks0, bge_embeddings)
    docs = knowledge_base0.similarity_search(question, k=5)
    combined_content = ''.join(doc.page_content + "\n" for doc in docs)
    return "文件中的相关信息如下：\n"+combined_content

class ebd_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {
                    "default": None
                }),
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),
                "file_content": ("STRING", {
                    "forceInput": True
                }),
                "device": (["cuda", "cpu"], {
                    "default": "cuda"
                })
            },
            "optional": {

            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "file"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"



    def file(self,path,file_content,is_enable="enable",device="cuda"):
        if is_enable=="disable":
            return (None,)
        global ebd_model,files_load,bge_embeddings
        files_load=file_content
        if ebd_model=="":
            model_kwargs = {'device': device}  # 如果您有GPU，可以设置为 'cuda'，否则使用 'cpu'
            encode_kwargs = {'normalize_embeddings': True}  # 设置为 True 以计算余弦相似度
        if bge_embeddings=="":
            bge_embeddings = HuggingFaceBgeEmbeddings(
                model_name=path,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
        output=[    {
    "type": "function",
  "function": {
    "name": "data_base",
    "description": "查询用户上传的文件中与用户提问相关的信息。",
    "parameters": {
      "type": "object",
      "properties": {
        "question": {"type": "string", "description": "要查询的关键词"},
      },
      "required": ["question"]
    }
  }
}]
        out=json.dumps(output, ensure_ascii=False)
        return (out,)