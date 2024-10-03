import json
import locale
import os
import requests
from bs4 import BeautifulSoup

# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
api_url=""
def search_searxng(query):
    global api_url
    if not api_url:
        api_url = "http://localhost:8080"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(f"{api_url}/search?q={query}", headers=headers)
    html_content = response.text

    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取搜索结果
    results = []
    for result in soup.find_all('article', class_='result'):
        title_tag = result.find('h3')
        link_tag = result.find('a', class_='url_wrapper')
        snippet_tag = result.find('p', class_='content')

        title = title_tag.get_text() if title_tag else 'No title'
        link = link_tag['href'] if link_tag else 'No link'
        snippet = snippet_tag.get_text() if snippet_tag else 'No snippet'

        results.append({
            'title': title,
            'link': link,
            'snippet': snippet
        })

    # 整合信息到一个字符串中
    result_str = ""
    for result in results:
        result_str += f"Title: {result['title']}\n"
        result_str += f"Link: {result['link']}\n"
        result_str += f"Snippet: {result['snippet']}\n"
        result_str += '-' * 40 + '\n'

    return result_str


class searxng_tool:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "searxng_api_url": ("STRING", {"default": "http://localhost:8080"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "query_searxng"

    CATEGORY = "大模型派对（llm_party）/工具（tools）"

    def query_searxng(self, searxng_api_url, is_enable=True):

        if not is_enable:
            return (None,)
        global api_url
        api_url = searxng_api_url
        output = [
            {
                "type": "function",
                "function": {
                    "name": "search_searxng",
                    "description": "使用searxng搜索引擎搜索",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "你要在searxng中搜索的关键词",
                            }
                        },
                        "required": ["query"],
                    },
                },
            }
        ]
        out = json.dumps(output, ensure_ascii=False)
        return (out,)
_TOOL_HOOKS = ["search_searxng"]
NODE_CLASS_MAPPINGS = {
    "searxng_tool": searxng_tool,
}
lang = locale.getdefaultlocale()[0]
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "searxng_tool": "searxng搜索工具"
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "searxng_tool": "searxng Search Tool"
    }