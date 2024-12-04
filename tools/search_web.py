import json
from datetime import date

import requests

from ..config import config_path, load_api_keys

api_keys = load_api_keys(config_path)
g_api_key = api_keys.get("google_api_key")
g_CSE_ID = api_keys.get("CSE_ID")
g_searchType = "web"


def search_web(keywords, paper_num=1):
    if paper_num == "":
        paper_num = 1
    today = str(date.today())
    global g_api_key, g_CSE_ID, g_searchType
    num_results = 10
    start = num_results * (int(paper_num) - 1) + 1
    try:
        base_url = "https://www.googleapis.com/customsearch/v1"
        if g_searchType == "image":
            params = {
                "key": g_api_key,
                "cx": g_CSE_ID,  # 替换为你自己的Custom Search Engine ID
                "num": num_results,
                "q": keywords if isinstance(keywords, str) else " ".join(keywords),
                "start": start,
                "searchType": g_searchType,
            }
        else:
            params = {
                "key": g_api_key,
                "cx": g_CSE_ID,  # 替换为你自己的Custom Search Engine ID
                "num": num_results,
                "q": keywords if isinstance(keywords, str) else " ".join(keywords),
                "start": start,
            }

        response = requests.get(base_url, params=params, timeout=10)
        # 打印HTTP状态码和响应内容以供调试
        print("Status code:", response.status_code)
        print("Response body:", response.text)

        data = response.json()
        all_content = ""
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                for item in data["items"]:
                    keyword = item["snippet"]
                    url = item["link"]
                    all_content += "/n/n" + json.dumps({"snippet": keyword, "link": url}, ensure_ascii=False, indent=4)

        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred: {e}"

    print(all_content)
    return (
        "今天的日期是"
        + today
        + "，当前网络的信息和信息来源的网址为：“"
        + str(all_content)
        + "”。/n如果以上信息中没有相关信息，你可以改变paper_num，查看下一页的信息。"
    )


class google_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image"], {"default": "web"}),
            },
            "optional": {
                "google_api_key": ("STRING", {}),
                "google_CSE_ID": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def web(self, searchType="web", google_api_key=None, google_CSE_ID=None, is_enable=True):
        if is_enable == False:
            return (None,)
        global g_api_key, g_CSE_ID, g_searchType
        g_searchType = searchType
        if google_api_key is not None and google_api_key != "":
            g_api_key = google_api_key
        else:
            g_api_key = api_keys.get("google_api_key")
        if google_CSE_ID is not None and google_CSE_ID != "":
            g_CSE_ID = google_CSE_ID
        else:
            g_CSE_ID = api_keys.get("CSE_ID")
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": f"通过关键词获得谷歌搜索上的{g_searchType}信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开",
                            },
                            "paper_num": {"type": "string", "description": "谷歌搜索的页码，可以改变paper_num用于翻页"},
                        },
                        "required": ["keywords", "paper_num"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class google_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image"], {"default": "web"}),
                "keywords": ("STRING", {}),
                "paper_num": ("INT", {"default": "1"}),
            },
            "optional": {
                "google_api_key": ("STRING", {}),
                "google_CSE_ID": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def web(self, keywords, paper_num=1, searchType="web", google_api_key=None, google_CSE_ID=None, is_enable=True):
        if is_enable == False:
            return (None,)
        global g_api_key, g_CSE_ID, g_searchType
        g_searchType = searchType
        if google_api_key is not None and google_api_key != "":
            g_api_key = google_api_key
        else:
            g_api_key = api_keys.get("google_api_key")
        if google_CSE_ID is not None and google_CSE_ID != "":
            g_CSE_ID = google_CSE_ID
        else:
            g_CSE_ID = api_keys.get("CSE_ID")
        out = search_web(keywords, paper_num)
        return (out,)


api_keys = load_api_keys(config_path)
b_api_key = api_keys.get("bing_api_key")
b_searchType = "web"
b_config_id=""
is_custom = False
def search_web_bing(keywords, paper_num):
    today = str(date.today())
    global b_api_key, b_searchType,b_config_id,is_custom
    num_results = 10
    start = num_results * (int(paper_num) - 1) + 1
    try:
        if is_custom == False:
            # 使用必应搜索API的基础URL
            if b_searchType == "web":
                base_url = "https://api.bing.microsoft.com/v7.0/search"
            elif b_searchType == "image":
                base_url = "https://api.bing.microsoft.com/v7.0/images/search"
            elif b_searchType == "video":
                base_url = "https://api.bing.microsoft.com/v7.0/videos/search"
            elif b_searchType == "news":
                base_url = "https://api.bing.microsoft.com/v7.0/news/search"
        else:
            if b_searchType == "web":
                base_url = "https://api.bing.microsoft.com/v7.0/custom/search"
            elif b_searchType == "image":
                base_url = "https://api.bing.microsoft.com/v7.0/custom/images/search"
            elif b_searchType == "video":
                base_url = "https://api.bing.microsoft.com/v7.0/custom/videos/search"
            elif b_searchType == "news":
                base_url = "https://api.bing.microsoft.com/v7.0/custom/news/search"
        headers = {"Ocp-Apim-Subscription-Key": b_api_key}
        if b_config_id != "":
            params = {
                "q": keywords if isinstance(keywords, str) else " ".join(keywords),
                "count": num_results,
                "offset": start,
                "customConfig": b_config_id
            }
        else:
            params = {
                "q": keywords if isinstance(keywords, str) else " ".join(keywords),
                "count": num_results,
                "offset": start,
            }

        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        # 打印HTTP状态码和响应内容以供调试
        print("Status code:", response.status_code)
        print("Response body:", response.text)

        all_content = ""
        if response.status_code == 200:
            data = response.json()
            if "webPages" in data:
                for item in data["webPages"]["value"]:
                    snippet = item["snippet"]
                    url = item["url"]
                    all_content += "/n/n" + json.dumps({"snippet": snippet, "link": url}, ensure_ascii=False, indent=4)

        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred: {e}"

    print(all_content)
    return (
        "今天的日期是"
        + today
        + "，当前网络的信息和信息来源的网址为：“"
        + str(all_content)
        + "”。\n如果以上信息中没有相关信息，你可以改变paper_num，查看下一页的信息。"
    )


# 类定义和方法保持不变，只需将google_tool更名为bing_tool，并更新相关注释
class bing_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image", "video", "news"], {"default": "web"}),
            },
            "optional": {
                "bing_api_key": ("STRING", {}),
                "custom_config_id": ("STRING", {}),
                "is_custom_api": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def web(self, searchType="web", bing_api_key=None, is_enable=True,custom_config_id="",is_custom_api=False):
        if is_enable == False:
            return (None,)
        global b_api_key, b_searchType,b_config_id,is_custom
        is_custom = is_custom_api
        b_config_id = custom_config_id
        b_searchType = searchType
        if bing_api_key is not None and bing_api_key != "":
            b_api_key = bing_api_key
        else:
            b_api_key = api_keys.get("bing_api_key")
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_web_bing",
                    "description": f"通过关键词获得必应搜索上的{b_searchType}信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开",
                            },
                            "paper_num": {"type": "string", "description": "必应搜索的页码，可以改变paper_num用于翻页"},
                        },
                        "required": ["keywords", "paper_num"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)


class bing_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image", "video", "news"], {"default": "web"}),
                "keywords": ("STRING", {}),
                "paper_num": ("INT", {"default": "1"}),
            },
            "optional": {
                "bing_api_key": ("STRING", {}),
                "custom_config_id": ("STRING", {}),
                "is_custom_api": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "web"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def web(self, keywords, paper_num=1, searchType="web", bing_api_key=None, is_enable=True,custom_config_id="", is_custom_api=False):
        if is_enable == False:
            return (None,)
        global b_api_key, b_searchType,b_config_id,is_custom
        is_custom = is_custom_api
        b_config_id = custom_config_id
        b_searchType = searchType
        if bing_api_key is not None and bing_api_key != "":
            b_api_key = bing_api_key
        else:
            b_api_key = api_keys.get("bing_api_key")

        out = search_web_bing(keywords, paper_num)
        return (out,)



ddg_searchType = "web"

def search_duckduckgo(keywords, paper_num=1):
    if paper_num == "":
        paper_num = 1
    today = str(date.today())
    global ddg_searchType
    num_results = 10
    start = num_results * (int(paper_num) - 1) + 1
    try:
        base_url = "https://api.duckduckgo.com/"
        params = {
            "q": keywords if isinstance(keywords, str) else " ".join(keywords),
            "format": "json",
            "no_redirect": 1,
            "no_html": 1,
            "skip_disambig": 1,
        }
        if ddg_searchType == "image":
            params["ia"] = "images"
        else:
            params["ia"] = "web"

        response = requests.get(base_url, params=params, timeout=10)
        print("Status code:", response.status_code)
        print("Response body:", response.text)

        data = response.json()
        all_content = ""
        if response.status_code == 200:
            if "RelatedTopics" in data:
                for item in data["RelatedTopics"]:
                    if "Text" in item and "FirstURL" in item:
                        keyword = item["Text"]
                        url = item["FirstURL"]
                        all_content += "\n\n" + json.dumps({"snippet": keyword, "link": url}, ensure_ascii=False, indent=4)
            elif "ImageResults" in data:
                for item in data["ImageResults"]:
                    if "Title" in item and "Image" in item:
                        keyword = item["Title"]
                        url = item["Image"]
                        all_content += "\n\n" + json.dumps({"snippet": keyword, "link": url}, ensure_ascii=False, indent=4)
            else:
                print("No relevant data found in the response.")
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Exception occurred: {e}"

    print(all_content)
    return (
        "今天的日期是"
        + today
        + "，当前网络的信息和信息来源的网址为：“"
        + str(all_content)
        + "”。\n如果以上信息中没有相关信息，你可以改变paper_num，查看下一页的信息。"
    )

class duckduckgo_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image"], {"default": "web"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "web"

    CATEGORY = "大模型派对（llm_party）/工具（tools）/联网（Networking）"

    def web(self, searchType="web", is_enable=True):
        if is_enable == False:
            return (None,)
        global ddg_searchType
        ddg_searchType = searchType
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_duckduckgo",
                    "description": f"通过关键词获得DuckDuckGo搜索上的{ddg_searchType}信息。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "需要搜索的关键词，可以是多个词语，多个词语之间用空格隔开，但是多个词语只能是一个概念，而不是多个概念，如果有多个概念应拆分开来，多次调用duckduckgo。duckduckgo只支持英文搜索！关键词必须是英文。",
                            },
                            "paper_num": {"type": "string", "description": "DuckDuckGo搜索的页码，可以改变paper_num用于翻页"},
                        },
                        "required": ["keywords", "paper_num"],
                    },
                },
            }
        ]

        out = json.dumps(output, ensure_ascii=False)
        return (out,)
    
class duckduckgo_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": ("BOOLEAN", {"default": True}),
                "searchType": (["web", "image"], {"default": "web"}),
                "keywords": ("STRING", {}),
                "paper_num": ("INT", {"default": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "web"

    CATEGORY = "大模型派对（llm_party）/知识库（knowbase）"

    def web(self, keywords, paper_num=1, searchType="web", is_enable=True):
        if is_enable == False:
            return (None,)
        global ddg_searchType
        ddg_searchType = searchType
        out = search_duckduckgo(keywords, paper_num)
        return (out,)