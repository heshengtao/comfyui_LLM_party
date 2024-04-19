from datetime import date
import json
import requests
from ..config import config_path,load_api_keys
api_keys = load_api_keys(config_path)
g_api_key = api_keys.get('google_api_key')
g_CSE_ID = api_keys.get('CSE_ID')
def search_web(keywords,paper_num,url=None):
    today = str(date.today())
    global g_api_key,g_CSE_ID
    num_results=10
    start=num_results*(int(paper_num)-1)+1
    try:
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": g_api_key,
            "cx": g_CSE_ID,  # 替换为你自己的Custom Search Engine ID
            "num": num_results,
            "q": keywords if isinstance(keywords, str) else " ".join(keywords),
            "start": start,
        }

        response = requests.get(base_url, params=params,timeout=10)
        # 打印HTTP状态码和响应内容以供调试
        print("Status code:", response.status_code)
        print("Response body:", response.text)

        data = response.json()
        all_content=""
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                for item in data["items"]:
                    keyword=item['snippet']
                    url=item["link"]
                    all_content +=json.dumps({"snippet":keyword,"link":url},ensure_ascii=False,indent=4)
                
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred: {e}"


    print(all_content)
    return "今天的日期是"+today+"，当前网络的信息和信息来源的网址为：“"+str(all_content)+"”。/n如果以上信息中没有相关信息，你可以改变paper_num，查看下一页的信息。"


class google_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),
            },
            "optional": {
                "google_api_key":("STRING", {
                    
                }),
                "google_CSE_ID": ("STRING", {
                    
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"



    def web(self,google_api_key=None,google_CSE_ID=None,is_enable="enable"):   
        if is_enable=="disable":
            return (None,)
        global g_api_key,g_CSE_ID
        if google_api_key is not None and google_api_key!="":
            g_api_key=google_api_key
        else:
            g_api_key=api_keys.get('google_api_key')
        if google_CSE_ID is not None and google_CSE_ID!="":
            g_CSE_ID=google_CSE_ID
        else:
            g_CSE_ID=api_keys.get('CSE_ID')
        output = [{
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "通过关键词获得谷歌搜索上的信息。",
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {"type": "string", "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开"},
                "paper_num": {"type": "string", "description": "谷歌搜索的页码，可以改变paper_num用于翻页"}
            },
            "required": ["keywords", "paper_num"]
        }
    }
}]

        out=json.dumps(output, ensure_ascii=False)
        return (out,)