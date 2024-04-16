from datetime import date
import json
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from langchain_community.vectorstores import FAISS
from ..config import bge_embeddings



def check_web(url, keyword):
    """
    获取网站页面上与关键词相关的文字信息。

    :param url: 网站的URL。
    :param keyword: 搜索的关键词。
    :return: 与关键词相关的文本内容。
    """
    text_splitter0 = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
    ) 
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 确保请求成功

        # 设置响应内容的编码，确保文本不会出现编码问题
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = ""
        for p in paragraphs:
            text += p.text

        # 查找包含关键词的文本
        #chunks0 = text_splitter0.split_text(text)
        #knowledge_base0 = FAISS.from_texts(chunks0, bge_embeddings)
        #docs = knowledge_base0.similarity_search(keyword, k=5)
        #combined_content = ''.join(doc.page_content + "\n" for doc in docs)
        combined_content =text
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
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),                
            },
            "optional": {
                "web_url": ("STRING",{

                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "read_web"

    #OUTPUT_NODE = False

    CATEGORY = "llm"



    def read_web(self,is_enable="enable",web_url=None):   
        if is_enable=="disable":
            return (None,)
        if web_url is None and web_url !="":
            output = [{
        "type": "function",
        "function": {
            "name": "check_web",
            "description": "通过关键词搜索一个给定url的网页上的信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "要被搜索的网页的URL，默认网址为"+web_url},
                    "keyword": {"type": "string", "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开"},

                },
                "required": ["url","keyword"]
            }
        }
    }]
            
        else:
            output = [{
        "type": "function",
        "function": {
            "name": "check_web",
            "description": "通过关键词搜索一个给定url的网页上的信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "要被搜索的网页的URL"},
                    "keyword": {"type": "string", "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开"},

                },
                "required": ["url","keyword"]
            }
        }
    }]

        out=json.dumps(output, ensure_ascii=False)
        return (out,)